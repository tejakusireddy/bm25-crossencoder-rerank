private function getRecursiveTraits($class = null)
    {
        if (null == $class) {
            $class = get_class($this);
        }

        $reflection = new \ReflectionClass($class);
        $traits = array_keys($reflection->getTraits());

        foreach ($traits as $trait) {
            $traits = array_merge($traits, $this->getRecursiveTraits($trait));
        }

        if ($parent = $reflection->getParentClass()) {
            $traits = array_merge($traits, $this->getRecursiveTraits($parent->getName()));
        }

        return $traits;
    }