function isLocalized($name,$lang=NULL) {
		if (!isset($lang))
			$lang=$this->current;
		return !$this->isGlobal($name) && array_key_exists($name,$this->_aliases) &&
				(!isset($this->rules[$lang][$name]) || $this->rules[$lang][$name]!==FALSE);
	}