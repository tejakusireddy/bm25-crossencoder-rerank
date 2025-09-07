public static function collectionOf(IType $elementType, string $collectionClass = ITypedCollection::class) : CollectionType
    {
        $elementTypeString = $elementType->asTypeString();

        if (!isset(self::$collections[$collectionClass][$elementTypeString])) {
            self::$collections[$collectionClass][$elementTypeString] = new CollectionType($elementType, $collectionClass);
        }

        return self::$collections[$collectionClass][$elementTypeString];
    }