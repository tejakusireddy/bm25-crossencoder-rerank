public function getControl()
	{
		$control = parent::getControl();
		$control->type = $this->htmlType;
		$control->addClass($this->htmlType);

		list($min, $max) = $this->extractRangeRule($this->getRules());
		if ($min instanceof DateTimeInterface) {
			$control->min = $min->format($this->htmlFormat);
		}
		if ($max instanceof DateTimeInterface) {
			$control->max = $max->format($this->htmlFormat);
		}
		$value = $this->getValue();
		if ($value instanceof DateTimeInterface) {
			$control->value = $value->format($this->htmlFormat);
		}

		return $control;
	}