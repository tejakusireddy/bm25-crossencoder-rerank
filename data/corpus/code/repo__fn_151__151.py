public static function has_ongoing_request($userid, $type) {
        global $DB;

        // Check if the user already has an incomplete data request of the same type.
        $nonpendingstatuses = [
            self::DATAREQUEST_STATUS_COMPLETE,
            self::DATAREQUEST_STATUS_CANCELLED,
            self::DATAREQUEST_STATUS_REJECTED,
            self::DATAREQUEST_STATUS_DOWNLOAD_READY,
            self::DATAREQUEST_STATUS_EXPIRED,
            self::DATAREQUEST_STATUS_DELETED,
        ];
        list($insql, $inparams) = $DB->get_in_or_equal($nonpendingstatuses, SQL_PARAMS_NAMED, 'st', false);
        $select = "type = :type AND userid = :userid AND status {$insql}";
        $params = array_merge([
            'type' => $type,
            'userid' => $userid
        ], $inparams);

        return data_request::record_exists_select($select, $params);
    }