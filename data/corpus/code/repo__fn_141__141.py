private function getTranslationGroups($lang = 'en'): void
    {
        $dir = resource_path('lang/'. $lang . '/');
        $files = array_diff(scandir($dir), array('..', '.'));

        foreach($files as $index => $filename){
            $groupname = str_replace(".php", "", $filename);
            $this->updateTranslationGroups($groupname);
        }

    }