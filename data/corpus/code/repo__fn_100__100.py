public function process(array $coveredIds) : void
    {
        $this->setCoveredPatternIds($coveredIds);

        $finder = new Finder();
        $finder->files();
        $finder->name('*.json');
        $finder->ignoreDotFiles(true);
        $finder->ignoreVCS(true);
        $finder->sortByName();
        $finder->ignoreUnreadableDirs();
        $finder->in($this->resourceDir);

        foreach ($finder as $file) {
            /* @var \Symfony\Component\Finder\SplFileInfo $file */

            /** @var string $patternFileName */
            $patternFileName = mb_substr($file->getPathname(), (int) mb_strpos($file->getPathname(), 'resources/'));

            if (!isset($this->coveredIds[$patternFileName])) {
                $this->coveredIds[$patternFileName] = [];
            }

            $this->coverage[$patternFileName] = $this->processFile(
                $patternFileName,
                $file->getContents(),
                $this->coveredIds[$patternFileName]
            );
        }
    }