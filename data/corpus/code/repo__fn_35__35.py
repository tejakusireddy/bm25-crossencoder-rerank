protected function getGroupedProfiles()
    {
        $this->analytics->requireAuthentication();

        $groupedProfiles = [];
        $accounts = $this->analytics->management_accounts->listManagementAccounts();
        foreach ($accounts as $account) {
            $groupedProfiles[$account->getId()]['label'] = $account->getName();
            $groupedProfiles[$account->getId()]['items'] = [];
        }
        $webproperties = $this->analytics->management_webproperties->listManagementWebproperties('~all');
        $webpropertiesById = [];
        foreach ($webproperties as $webproperty) {
            $webpropertiesById[$webproperty->getId()] = $webproperty;
        }
        $profiles = $this->analytics->management_profiles->listManagementProfiles('~all', '~all');
        foreach ($profiles as $profile) {
            if (isset($webpropertiesById[$profile->getWebpropertyId()])) {
                $webproperty = $webpropertiesById[$profile->getWebpropertyId()];
                $groupedProfiles[$profile->getAccountId()]['items'][$profile->getId()] = ['label' => $webproperty->getName() . ' > ' . $profile->getName(), 'value' => $profile->getId()];
            }
        }

        return $groupedProfiles;
    }