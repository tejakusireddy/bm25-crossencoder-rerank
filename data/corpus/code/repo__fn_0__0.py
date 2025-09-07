protected function parentId()
	{
		switch ( $this->position )
		{
			case 'root':
				return null;

			case 'child':
				return $this->target->getKey();

			default:
				return $this->target->getParentId();
		}
	}