public function valid() : bool
    {
        if ($this->pointer >= 0 && $this->pointer < count($this->members)) {
            return true;
        }
        return false;
    }