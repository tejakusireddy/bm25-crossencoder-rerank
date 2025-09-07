public function getPattern(PackageInterface $package)
    {
        if (isset($this->packages[$package->getName()])) {
            return $this->packages[$package->getName()];
        } elseif (isset($this->packages[$package->getPrettyName()])) {
            return $this->packages[$package->getPrettyName()];
        } elseif (isset($this->types[$package->getType()])) {
            return $this->types[$package->getType()];
        }
    }