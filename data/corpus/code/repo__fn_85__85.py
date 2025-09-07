public function createProcedure($name)
    {
        $definition = array(
            'parent' => $this->context,
            'name' => $name,
            'sources' => array(),
            'workers' => array(),
            'targets' => array(),
            'children' => array(),
        );

        $this->definitions[$name] = $definition;

        $this->context = $name;

        return $this;
    }