func Digests(key Trits, spongeFunc ...SpongeFunction) (Trits, error) {
	var err error
	fragments := int(math.Floor(float64(len(key)) / KeyFragmentLength))
	digests := make(Trits, fragments*HashTrinarySize)
	buf := make(Trits, HashTrinarySize)

	h := GetSpongeFunc(spongeFunc, kerl.NewKerl)
	defer h.Reset()

	// iterate through each key fragment
	for i := 0; i < fragments; i++ {
		keyFragment := key[i*KeyFragmentLength : (i+1)*KeyFragmentLength]

		// each fragment consists of 27 segments
		for j := 0; j < KeySegmentsPerFragment; j++ {
			copy(buf, keyFragment[j*HashTrinarySize:(j+1)*HashTrinarySize])

			// hash each segment 26 times
			for k := 0; k < KeySegmentHashRounds; k++ {
				h.Absorb(buf)
				buf, err = h.Squeeze(HashTrinarySize)
				if err != nil {
					return nil, err
				}
				h.Reset()
			}

			copy(keyFragment[j*HashTrinarySize:], buf)
		}

		// hash the key fragment (which now consists of hashed segments)
		if err := h.Absorb(keyFragment); err != nil {
			return nil, err
		}

		buf, err := h.Squeeze(HashTrinarySize)
		if err != nil {
			return nil, err
		}

		copy(digests[i*HashTrinarySize:], buf)

		h.Reset()
	}

	return digests, nil
}