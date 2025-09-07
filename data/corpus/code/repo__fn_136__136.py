public function put($key, $value, $minutes)
    {
        $this->forever($key, $value);
        $this->redis->expire($key, $minutes * 60);
    }