func (wp WeightedPages) Prev(cur Page) Page {
	for x, c := range wp {
		if c.Page == cur {
			if x == 0 {
				return wp[len(wp)-1].Page
			}
			return wp[x-1].Page
		}
	}
	return nil
}