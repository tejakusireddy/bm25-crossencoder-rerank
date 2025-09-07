func (p *parser) readv(t token) ([]token, error) {
	var tokens []token
	for {
		read, err := p.readt(t.typ)
		tokens = append(tokens, read...)
		if err != nil {
			return tokens, err
		}
		if len(read) > 0 && read[len(read)-1].val == t.val {
			break
		}
	}
	return tokens, nil
}