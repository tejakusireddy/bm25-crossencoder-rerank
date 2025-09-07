protected function unserializeEmbeddedCollection(MapperInterface $mapper, array $data)
    {
        $collection = array();
        foreach ($data as $document) {
            $collection[] = $mapper->unserialize($document);
        }

        return $collection;
    }