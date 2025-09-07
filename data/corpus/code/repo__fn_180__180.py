public function setElements(array $elements)
    {
        $this->elements = [];
        foreach ($elements as $name => $element) {
            $this->setElement($name, $element);
        }

        return $this;
    }