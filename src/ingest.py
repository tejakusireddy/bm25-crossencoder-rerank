#!/usr/bin/env python3
"""
Ingest & Chunk → OpenSearch Indexer for LLM Reranker

Usage (local):
  python src/ingest.py \
    --input data/corpus \
    --index llm_reranker \
    --host http://localhost:9200 \
    --batch 750 --chunk_chars 1500 --overlap_chars 150 \
    --purge

Notes:
- Code-aware chunking for common languages; markdown heading-aware for docs.
- Stores metadata (repo, path, language, symbol/heading, chunk_index).
- Idempotent: content-hash de-dup per (path + chunk_text).
- Designed for fast BM25 baselines; dense indexing can be added separately.
"""

from __future__ import annotations
import argparse
import hashlib
import os
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from opensearchpy import OpenSearch, helpers
from tqdm import tqdm

# -----------------------------
# Language detection by extension
# -----------------------------
EXT2LANG = {
    ".py": "python",
    ".java": "java",
    ".go": "go",
    ".js": "javascript",
    ".ts": "typescript",
    ".jsx": "javascript",
    ".tsx": "typescript",
    ".rb": "ruby",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".c": "c",
    ".cs": "csharp",
    ".php": "php",
    ".rs": "rust",
    ".kt": "kotlin",
    ".scala": "scala",
    ".md": "markdown",
    ".mdx": "markdown",
    ".txt": "text",
}

# -----------------------------
# Regex splitters (lightweight, fast)
# -----------------------------
PY_SIG = re.compile(r"^\s*(def|class)\s+([A-Za-z_][\w]*)", re.MULTILINE)
JAVA_SIG = re.compile(
    r"^\s*(?:public|protected|private|static|final|abstract|synchronized|native|strictfp|\s)*\s*(?:class|interface|enum|@interface)\s+\w+|^\s*(?:public|protected|private|static|final|native|synchronized|abstract|\s)*\s*\w+[\<\w\>\[\]]*\s+\w+\s*\([^)]*\)\s*\{?",
    re.MULTILINE,
)
JS_TS_SIG = re.compile(
    r"^\s*(?:export\s+)?(?:async\s+)?function\s+\w+\s*\(|^\s*class\s+\w+|^\s*const\s+\w+\s*=\s*\((?:.|\n)*?\)\s*=>",
    re.MULTILINE,
)
GO_SIG = re.compile(r"^\s*func\s+(?:\([^)]*\)\s*)?\w+\s*\(.*\)", re.MULTILINE)
MD_HEADING = re.compile(r"^(#{1,6})\s+(.+)", re.MULTILINE)

# -----------------------------
# Index settings/mappings (BM25)
# -----------------------------
DEF_SETTINGS = {
    "settings": {
        "index": {"number_of_shards": 1, "number_of_replicas": 0},
        "analysis": {
            "analyzer": {
                "default": {"type": "standard"},
                "path_analyzer": {
                    "type": "custom",
                    "tokenizer": "path_hierarchy",
                    "filter": ["lowercase"],
                },
            }
        },
    },
    "mappings": {
        "properties": {
            "text": {"type": "text", "store": True},
            "repo": {"type": "keyword"},
            "path": {"type": "text", "analyzer": "path_analyzer"},
            "language": {"type": "keyword"},
            "symbol": {"type": "text", "fields": {"raw": {"type": "keyword"}}},
            "heading": {"type": "text", "fields": {"raw": {"type": "keyword"}}},
            "chunk_index": {"type": "integer"},
            "n_chars": {"type": "integer"},
            "content_sha1": {"type": "keyword"},
        }
    },
}

# -----------------------------
# Helpers
# -----------------------------

def norm_text(s: str) -> str:
    return "\n".join(line.rstrip() for line in s.strip().splitlines())


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()


def guess_repo(root: Path, file_path: Path) -> str:
    try:
        rel = file_path.relative_to(root)
        # repo guessed as first-level directory under input root
        parts = rel.parts
        return parts[0] if len(parts) > 1 else root.name
    except Exception:
        return root.name


def read_text(path: Path, max_bytes: int) -> str:
    with open(path, "rb") as f:
        b = f.read(max_bytes + 1)
    return b[:max_bytes].decode("utf-8", errors="ignore")


# -----------------------------
# Chunkers
# -----------------------------

def split_on_regex(text: str, pat: re.Pattern, min_chunk: int, max_chunk: int, overlap: int) -> List[str]:
    """Generic regex-based splitter; falls back to windowed chunks if gigantic blocks."""
    idxs = [m.start() for m in pat.finditer(text)]
    if not idxs:
        return window_chunks(text, max_chunk, overlap)

    idxs.append(len(text))
    chunks: List[str] = []
    for i in range(len(idxs) - 1):
        seg = text[idxs[i] : idxs[i + 1]]
        seg = seg.strip()
        if not seg:
            continue
        if len(seg) <= max_chunk:
            chunks.append(seg)
        else:
            chunks.extend(window_chunks(seg, max_chunk, overlap))
    # Merge tiny tails
    merged: List[str] = []
    buf = ""
    for c in chunks:
        if len(buf) + len(c) < min_chunk:
            buf += ("\n\n" if buf else "") + c
        else:
            if buf:
                merged.append(buf)
                buf = ""
            merged.append(c)
    if buf:
        merged.append(buf)
    return merged


def window_chunks(text: str, max_chunk: int, overlap: int) -> List[str]:
    if len(text) <= max_chunk:
        return [text.strip()]
    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = min(start + max_chunk, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = max(0, end - overlap)
    return chunks


def md_heading_chunks(text: str, max_chunk: int, overlap: int) -> List[Tuple[str, Optional[str]]]:
    """Return (chunk, heading) pairs for markdown."""
    positions = [(m.start(), m.group(2).strip()) for m in MD_HEADING.finditer(text)]
    if not positions:
        return [(c, None) for c in window_chunks(text, max_chunk, overlap)]

    positions.append((len(text), None))
    out: List[Tuple[str, Optional[str]]] = []
    for i in range(len(positions) - 1):
        s, head = positions[i]
        e, _ = positions[i + 1]
        block = text[s:e].strip()
        for c in window_chunks(block, max_chunk, overlap):
            out.append((c, head))
    return out


def code_chunks(text: str, lang: str, min_chunk: int, max_chunk: int, overlap: int) -> List[Tuple[str, Optional[str]]]:
    pat = None
    if lang == "python":
        pat = PY_SIG
    elif lang == "java":
        pat = JAVA_SIG
    elif lang in {"javascript", "typescript"}:
        pat = JS_TS_SIG
    elif lang == "go":
        pat = GO_SIG

    if pat is None:
        return [(c, None) for c in window_chunks(text, max_chunk, overlap)]

    segs = split_on_regex(text, pat, min_chunk, max_chunk, overlap)
    # Symbol extraction: first line signature if present
    out: List[Tuple[str, Optional[str]]] = []
    for seg in segs:
        first = seg.splitlines()[0] if seg else ""
        m = pat.match(first)
        sym = None
        if m:
            # best-effort: last word-like token in signature line
            cand = m.group(0).strip()
            toks = re.findall(r"[A-Za-z_][\w]*", cand)
            sym = toks[-1] if toks else None
        out.append((seg, sym))
    return out


# -----------------------------
# Index creation
# -----------------------------

def ensure_index(client: OpenSearch, index: str, purge: bool = False) -> None:
    if purge and client.indices.exists(index=index):
        client.indices.delete(index=index, ignore=[400, 404])
    if not client.indices.exists(index=index):
        client.indices.create(index=index, body=DEF_SETTINGS)


# -----------------------------
# Document generator
# -----------------------------

def iter_files(root: Path) -> Iterable[Path]:
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in EXT2LANG:
            continue
        yield p


def build_docs(
    root: Path,
    index: str,
    path: Path,
    max_bytes: int,
    min_chunk: int,
    max_chunk: int,
    overlap: int,
) -> Iterable[Dict]:
    text = read_text(path, max_bytes)
    if not text.strip():
        return

    lang = EXT2LANG.get(path.suffix.lower(), "text")
    repo = guess_repo(root, path)
    rel_path = str(path.relative_to(root))

    if lang == "markdown":
        pairs = md_heading_chunks(text, max_chunk, overlap)
    elif lang == "text":
        pairs = [(c, None) for c in window_chunks(text, max_chunk, overlap)]
    else:
        pairs = code_chunks(text, lang, min_chunk, max_chunk, overlap)

    for i, (chunk, tag) in enumerate(pairs):
        chunk_norm = norm_text(chunk)
        if not chunk_norm:
            continue
        content_hash = sha1(rel_path + "\n" + chunk_norm)
        doc_id = sha1(rel_path + f"#:{i}")
        doc = {
            "_index": index,
            "_id": doc_id,
            "_source": {
                "text": chunk_norm,
                "repo": repo,
                "path": rel_path,
                "language": lang,
                "symbol": tag if lang != "markdown" else None,
                "heading": tag if lang == "markdown" else None,
                "chunk_index": i,
                "n_chars": len(chunk_norm),
                "content_sha1": content_hash,
            },
        }
        yield doc


# -----------------------------
# Main
# -----------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=str, required=True, help="Path to corpus root")
    ap.add_argument("--index", type=str, default="llm_reranker")
    ap.add_argument("--host", type=str, default="http://localhost:9200")
    ap.add_argument("--user", type=str, default=None)
    ap.add_argument("--password", type=str, default=None)
    ap.add_argument("--batch", type=int, default=750, help="Bulk batch size")
    ap.add_argument("--max_bytes", type=int, default=1_500_000, help="Max bytes per file")
    ap.add_argument("--chunk_chars", type=int, default=1500)
    ap.add_argument("--overlap_chars", type=int, default=150)
    ap.add_argument("--min_chunk_chars", type=int, default=600)
    ap.add_argument("--purge", action="store_true", help="Delete and recreate index")
    args = ap.parse_args()

    root = Path(args.input).resolve()
    if not root.exists():
        print(f"[ERR] Input path not found: {root}", file=sys.stderr)
        sys.exit(2)

    client = OpenSearch(
        hosts=[args.host],
        http_auth=(args.user, args.password) if args.user and args.password else None,
        timeout=60,
        max_retries=5,
        retry_on_timeout=True,
    )

    # sanity ping
    try:
        client.info()
    except Exception as e:
        print(f"[ERR] Cannot connect to OpenSearch at {args.host}: {e}", file=sys.stderr)
        sys.exit(2)

    ensure_index(client, args.index, purge=args.purge)

    paths = list(iter_files(root))
    if not paths:
        print(f"[WARN] No files found under {root}")
        return

    def _docs() -> Iterable[Dict]:
        for p in paths:
            yield from build_docs(
                root,
                args.index,
                p,
                args.max_bytes,
                args.min_chunk_chars,
                args.chunk_chars,
                args.overlap_chars,
            )

    print(f"[INFO] Indexing {len(paths)} files from {root} → index '{args.index}'")
    success, failed = helpers.bulk(
        client,
        _docs(),
        chunk_size=args.batch,
        request_timeout=120,
        raise_on_error=False,
        stats_only=True,
    )
    print(f"[DONE] Indexed docs: {success}; failed: {failed}")


if __name__ == "__main__":
    main()
