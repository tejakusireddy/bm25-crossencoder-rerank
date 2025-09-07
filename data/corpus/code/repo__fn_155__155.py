public function save($config)
    {
        if (!file_put_contents($this->filename, Yaml::dump($config))) {
            return false;
        }
        return true;
    }