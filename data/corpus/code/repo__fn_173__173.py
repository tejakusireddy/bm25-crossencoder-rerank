private function updateStorage($with = [])
    {
        $data = array_merge($this->data, $with);
        $this->fs->create($this->fsPath, json_encode($data));
    }