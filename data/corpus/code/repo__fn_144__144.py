func NewTOTP(key []byte, start uint64, step uint64, digits int, algo crypto.Hash) *TOTP {
	h := hashFromAlgo(algo)
	if h == nil {
		return nil
	}

	return &TOTP{
		OATH: &OATH{
			key:     key,
			counter: start,
			size:    digits,
			hash:    h,
			algo:    algo,
		},
		step: step,
	}

}