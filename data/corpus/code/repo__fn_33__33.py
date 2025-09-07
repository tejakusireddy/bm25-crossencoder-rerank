public function getInArray($name, array $array)
    {
        $value = $this->get($name);
        return in_array($value, $array) ? $value : $array[key($array)];
    }