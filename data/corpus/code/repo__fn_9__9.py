public function addSettingItems($owner, array $definitions)
    {
        foreach ($definitions as $code => $definition) {
            $this->addSettingItem($owner, $code, $definition);
        }
    }