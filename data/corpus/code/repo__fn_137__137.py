protected function createComponent($name): ?IComponent
    {
        $method = 'createComponent'.ucfirst($name);
        if (method_exists($this, $method)) {
            $this->checkRequirements(self::getReflection()->getMethod($method));
        }

        return parent::createComponent($name);
    }