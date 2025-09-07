func FallbackAddr(fallbackAddr btcutil.Address) func(*Invoice) {
	return func(i *Invoice) {
		i.FallbackAddr = fallbackAddr
	}
}