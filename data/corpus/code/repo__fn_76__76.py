public function addLimitOffset(int $limit, int $offset): void
    {
        if ($limit === 0 && $offset === 0) {
            return;
        }
        if ($limit === 0 && $offset <> 0) {
            return;
        }
        if ($offset === 0) {
            $this->statement .= ' LIMIT ' . $limit;
        } else {
            $this->statement .= sprintf(' LIMIT %d, %d', $offset, $limit);
        }
        $this->statement .= PHP_EOL;
    }