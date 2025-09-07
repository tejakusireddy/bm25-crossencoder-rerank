public function verifyPhone(): bool
    {
        $phone = new UserMetaPhone($this->notification_phone);
        $phone->verifyPhone();
        $this->notification_phone = $phone;
        return $this->updateModel();
    }