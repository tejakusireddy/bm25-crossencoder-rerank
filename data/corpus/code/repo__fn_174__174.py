func drawCondFmtCellIs(p int, ct string, format *formatConditional) *xlsxCfRule {
	c := &xlsxCfRule{
		Priority: p + 1,
		Type:     validType[format.Type],
		Operator: ct,
		DxfID:    &format.Format,
	}
	// "between" and "not between" criteria require 2 values.
	_, ok := map[string]bool{"between": true, "notBetween": true}[ct]
	if ok {
		c.Formula = append(c.Formula, format.Minimum)
		c.Formula = append(c.Formula, format.Maximum)
	}
	_, ok = map[string]bool{"equal": true, "notEqual": true, "greaterThan": true, "lessThan": true}[ct]
	if ok {
		c.Formula = append(c.Formula, format.Value)
	}
	return c
}