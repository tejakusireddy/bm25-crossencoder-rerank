func Range(str string, params ...string) bool {
	if len(params) == 2 {
		value, _ := ToFloat(str)
		min, _ := ToFloat(params[0])
		max, _ := ToFloat(params[1])
		return InRange(value, min, max)
	}

	return false
}