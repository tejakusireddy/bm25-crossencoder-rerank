public function setDisplayBank($displayBank = true)
    {
        $this->isBool($displayBank, 'displayBank');
        $this->displayBank = $displayBank;

        return $this;
    }