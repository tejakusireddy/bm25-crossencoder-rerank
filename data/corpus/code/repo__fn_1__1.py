func (p *MediaPlaylist) SetWinSize(winsize uint) error {
	if winsize > p.capacity {
		return errors.New("capacity must be greater than winsize or equal")
	}
	p.winsize = winsize
	return nil
}