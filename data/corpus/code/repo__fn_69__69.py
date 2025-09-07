public function getBehaviors()
    {
        if (null === $this->behaviors) {
            // find behaviors in composer.lock file
            $lock = $this->findComposerLock();

            if (null === $lock) {
                $this->behaviors = [];
            } else {
                $this->behaviors = $this->loadBehaviors($lock);
            }

            // find behavior in composer.json (useful when developing a behavior)
            $json = $this->findComposerJson();

            if (null !== $json) {
                $behavior = $this->loadBehavior(json_decode($json->getContents(), true));

                if (null !== $behavior) {
                    $this->behaviors[$behavior['name']] = $behavior;
                }
            }
        }

        return $this->behaviors;
    }