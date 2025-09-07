public function getAssociationLabels(RepositoryInterface $table) : array
    {
        /** @var \Cake\ORM\Table */
        $table = $table;

        $result = [];
        foreach ($table->associations() as $association) {
            if (!in_array($association->type(), $this->searchableAssociations)) {
                continue;
            }

            $result[$association->getName()] = Inflector::humanize(current((array)$association->getForeignKey()));
        }

        return $result;
    }