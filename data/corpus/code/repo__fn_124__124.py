func (s *AtomicSequence) Load(data []byte) error {
	if s.initialized {
		return errors.New("cannot load into an initialized sequence")
	}

	vals := make(map[string]uint64)
	if err := json.Unmarshal(data, &vals); err != nil {
		return err
	}

	if val, ok := vals["current"]; !ok {
		return errors.New("improperly formatted data or sequence version")
	} else {
		atomic.SwapUint64(&s.current, val)
	}

	if val, ok := vals["increment"]; !ok {
		return errors.New("improperly formatted data or sequence version")
	} else {
		atomic.SwapUint64(&s.increment, val)
	}

	if val, ok := vals["minvalue"]; !ok {
		return errors.New("improperly formatted data or sequence version")
	} else {
		atomic.SwapUint64(&s.minvalue, val)
	}

	if val, ok := vals["maxvalue"]; !ok {
		return errors.New("improperly formatted data or sequence version")
	} else {
		atomic.SwapUint64(&s.maxvalue, val)
	}

	s.initialized = true
	return nil
}