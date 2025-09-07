public function setHash(string $value) : User
    {

        if ($this->data['hash'] !== $value) {
            $this->data['hash'] = $value;
            $this->setModified('hash');
        }

        return $this;
    }