public function register_action_map($map)
    {
        if (is_array($map)) {
            foreach ($map as $idx => $val) {
                $this->action_map[$idx] = $val;
            }
        }
    }