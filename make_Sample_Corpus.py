#!/usr/bin/env python3
"""
Create a tiny local corpus for the LLM Reranker demo.

- Tries multiple public mirrors (no dead S3 links).
- Writes .py files to data/corpus/code/
- Adds a few docs to data/corpus/docs/
- Optionally creates starter queries.tsv and qrels.tsv

Usage:
  # Export first 800 examples (recommended)
  python scripts/make_sample_corpus.py --n 800 --with_qrels

  # Or export 1% of dataset (integer only)
  python scripts/make_sample_corpus.py --pct 1 --with_qrels
"""

import argparse
from pathlib import Path
import re
import sys

try:
    from datasets import load_dataset
except Exception:
    print("[ERR] Please install 'datasets' first: pip install -U datasets", file=sys.stderr)
    raise

SAFE = re.compile(r"[^a-zA-Z0-9_.-]+")


def safe(s: str, default: str = "snippet") -> str:
    s = (s or "").strip()
    s = SAFE.sub("_", s)[:120]
    return s or default


def write_docs(out_docs: Path) -> None:
    out_docs.mkdir(parents=True, exist_ok=True)
    (out_docs / "mysql.md").write_text(
        "# MySQL Connection Guide\nUse a connection string and credentials to connect safely.\n",
        encoding="utf-8",
    )
    (out_docs / "k8s.md").write_text(
        "# Kubernetes Service vs Ingress\nIngress manages external access; Service exposes pods.\n",
        encoding="utf-8",
    )


def export_from_dataset(dataset_name: str, config: str | None, split_spec: str, out_code: Path) -> int:
    written = 0
    ds = load_dataset(dataset_name, config, split=split_spec)
    for i, row in enumerate(ds):
        code = (row.get("code") or "").strip()
        if not code:
            continue
        repo = safe((row.get("repo") or "repo").split("/")[-1], "repo")
        func = safe(row.get("func_name") or row.get("func_name_str") or f"fn_{i}")
        (out_code / f"{repo}__{func}__{i}.py").write_text(code, encoding="utf-8")
        written += 1
    return written


def export_codesearchnet_python(out_code: Path, n: int | None, pct: int | None) -> int:
    """Try mirrors in order; return number of files written."""
    if n and n > 0:
        split_spec = f"train[:{n}]"
    elif pct and 1 <= pct <= 100:
        split_spec = f"train[:{pct}%]"
    else:
        split_spec = "train[:500]"

    # 1) Nan-Do parquet mirror
    try:
        return export_from_dataset("Nan-Do/code-search-net-python", None, split_spec, out_code)
    except Exception as e:
        print(f"[WARN] Nan-Do/code-search-net-python failed: {e}")

    # 2) sentence-transformers mirror
    try:
        return export_from_dataset("sentence-transformers/codesearchnet", "pair", split_spec, out_code)
    except Exception as e:
        print(f"[WARN] sentence-transformers/codesearchnet failed: {e}")

    # 3) Fallback synthetic samples
    samples = [
        ("demo_repo", "connect_mysql",
         "def connect_mysql(h,u,p):\n    import mysql.connector\n    return mysql.connector.connect(host=h,user=u,password=p)\n"),
        ("demo_repo", "http_get",
         "import requests\n\ndef http_get(url):\n    r = requests.get(url, timeout=5)\n    return r.text\n"),
    ]
    for i, (repo, func, code) in enumerate(samples):
        (out_code / f"{repo}__{func}__{i}.py").write_text(code, encoding="utf-8")
    return len(samples)


def maybe_write_qrels(root: Path) -> None:
    queries = root / "data/queries.tsv"
    qrels = root / "data/qrels.tsv"
    if not queries.exists():
        queries.write_text(
            "q1\tpython mysql connect\nq2\tpython http get request\n",
            encoding="utf-8",
        )
    if not qrels.exists():
        qrels.write_text("", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=800, help="Number of examples to export")
    ap.add_argument("--pct", type=int, default=None, help="Percentage of split (integer 1..100)")
    ap.add_argument("--with_qrels", action="store_true", help="Create starter queries/qrels")
    args = ap.parse_args()

    root = Path(".").resolve()
    out_code = root / "data/corpus/code"
    out_docs = root / "data/corpus/docs"
    out_code.mkdir(parents=True, exist_ok=True)

    n_written = export_codesearchnet_python(out_code, args.n, args.pct)
    write_docs(out_docs)

    if args.with_qrels:
        maybe_write_qrels(root)

    print(f"[DONE] Wrote {n_written} code files → {out_code}")
    print(f"[DONE] Wrote docs → {out_docs}")
    if args.with_qrels:
        print("[INFO] Starter queries.tsv/qrels.tsv created under data/")


if __name__ == "__main__":
    main()
