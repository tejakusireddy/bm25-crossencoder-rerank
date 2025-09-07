public static function isHostKnownAliasHost($urlHost, $idSite)
    {
        $websiteData = Cache::getCacheWebsiteAttributes($idSite);

        if (isset($websiteData['hosts'])) {
            $canonicalHosts = array();
            foreach ($websiteData['hosts'] as $host) {
                $canonicalHosts[] = self::toCanonicalHost($host);
            }

            $canonicalHost = self::toCanonicalHost($urlHost);
            if (in_array($canonicalHost, $canonicalHosts)) {
                return true;
            }
        }

        return false;
    }