public function sortBy( \Closure $callback, bool $save_keys = true )
	{
		$items = $this->items;
		$save_keys ? uasort($items, $callback) : usort($items, $callback);
		return new static($items);
	}