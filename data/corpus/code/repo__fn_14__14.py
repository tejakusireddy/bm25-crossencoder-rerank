func (c Caser) Transform(dst, src []byte, atEOF bool) (nDst, nSrc int, err error) {
	nSrc = len(src) // Always read all the bytes of src
	result := c.Bytes(src)
	if len(result) > len(dst) {
		err = transform.ErrShortDst
	}
	nDst = copy(dst, result)
	return
}