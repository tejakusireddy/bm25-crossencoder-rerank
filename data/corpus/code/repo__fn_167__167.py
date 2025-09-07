protected function checkBrowserCustom()
    {
        foreach ($this->_customBrowserDetection as $browserName => $customBrowser) {
            $uaNameToLookFor = $customBrowser['uaNameToLookFor'];
            $isMobile = $customBrowser['isMobile'];
            $isRobot = $customBrowser['isRobot'];
            $separator = $customBrowser['separator'];
            $uaNameFindWords = $customBrowser['uaNameFindWords'];
            if ($this->checkSimpleBrowserUA($uaNameToLookFor, $this->_agent, $browserName, $isMobile, $isRobot, $separator, $uaNameFindWords)) {
                return true;
            }
        }
        return false;
    }