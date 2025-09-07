function parse_lpstr(blob, type, pad) {
	var start = blob.l;
	var str = blob.read_shift(0, 'lpstr-cp');
	if(pad) while((blob.l - start) & 3) ++blob.l;
	return str;
}