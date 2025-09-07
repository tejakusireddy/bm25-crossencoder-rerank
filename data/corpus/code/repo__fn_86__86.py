protected function convert($to, $val)
    {
        $val = $this->parseValue($val);

        return base_convert($val, $this->unit, $to);
    }