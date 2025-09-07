public function getSiteRole($nb_site_role)
    {
        if (is_numeric($nb_role_id = nb_getMixedValue($nb_site_role, NABU_ROLE_FIELD_ID))) {
            $retval = $this->getSiteRoles()->getItem($nb_role_id);
        } else {
            $retval = false;
        }

        return $retval;
    }