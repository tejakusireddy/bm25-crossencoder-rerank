public static function getLocales($domain = null)
    {
        // Optionally filter by domain
        $domainObj = Domain::getByDomain($domain);
        if ($domainObj) {
            return $domainObj->getLocales();
        }

        return Locale::getCached();
    }