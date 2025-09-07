protected function clearIDList()
    {
        $arCacheTags = $this->getCacheTagList();
        $sCacheKey = $this->getCacheKey();

        CCache::clear($arCacheTags, $sCacheKey);
    }