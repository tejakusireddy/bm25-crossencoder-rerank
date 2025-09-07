public function getChangedFiles($rev)
    {
        $raw_changes = $this->execute('hg status --change ' . $rev);
        $this->repository_type = 'hg';

        $changes = [];
        foreach ($raw_changes as $key => $change) {
            $exploded_change = explode(' ', $change);
            $changes[$key]['type'] = $exploded_change[0];
            $changes[$key]['path'] = $exploded_change[1];
        }

        return $changes;
    }