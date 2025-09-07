public function checks($name, $arg = null) {
        if (empty($arg)) {
            $this->checks[] = $name;
        } else {
            $this->checks[$name] = $arg;
        }
        return $this;
    }