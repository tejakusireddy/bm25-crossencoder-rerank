public function server(string $index = '', $xss_clean = false)
    {
        return $this->fetchFromArray($_SERVER, $index, $xss_clean);
    }