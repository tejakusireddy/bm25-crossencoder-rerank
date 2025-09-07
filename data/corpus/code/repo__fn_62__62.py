public function get_comments($page = '') {
        global $DB, $CFG, $USER, $OUTPUT;
        if (!$this->can_view()) {
            return false;
        }
        if (!is_numeric($page)) {
            $page = 0;
        }
        $params = array();
        $perpage = (!empty($CFG->commentsperpage))?$CFG->commentsperpage:15;
        $start = $page * $perpage;
        $ufields = user_picture::fields('u');

        list($componentwhere, $component) = $this->get_component_select_sql('c');
        if ($component) {
            $params['component'] = $component;
        }

        $sql = "SELECT $ufields, c.id AS cid, c.content AS ccontent, c.format AS cformat, c.timecreated AS ctimecreated
                  FROM {comments} c
                  JOIN {user} u ON u.id = c.userid
                 WHERE c.contextid = :contextid AND
                       c.commentarea = :commentarea AND
                       c.itemid = :itemid AND
                       $componentwhere
              ORDER BY c.timecreated DESC";
        $params['contextid'] = $this->contextid;
        $params['commentarea'] = $this->commentarea;
        $params['itemid'] = $this->itemid;

        $comments = array();
        $formatoptions = array('overflowdiv' => true, 'blanktarget' => true);
        $rs = $DB->get_recordset_sql($sql, $params, $start, $perpage);
        foreach ($rs as $u) {
            $c = new stdClass();
            $c->id          = $u->cid;
            $c->content     = $u->ccontent;
            $c->format      = $u->cformat;
            $c->timecreated = $u->ctimecreated;
            $c->strftimeformat = get_string('strftimerecentfull', 'langconfig');
            $url = new moodle_url('/user/view.php', array('id'=>$u->id, 'course'=>$this->courseid));
            $c->profileurl = $url->out(false); // URL should not be escaped just yet.
            $c->fullname = fullname($u);
            $c->time = userdate($c->timecreated, $c->strftimeformat);
            $c->content = format_text($c->content, $c->format, $formatoptions);
            $c->avatar = $OUTPUT->user_picture($u, array('size'=>18));
            $c->userid = $u->id;

            $candelete = $this->can_delete($c->id);
            if (($USER->id == $u->id) || !empty($candelete)) {
                $c->delete = true;
            }
            $comments[] = $c;
        }
        $rs->close();

        if (!empty($this->plugintype)) {
            // moodle module will filter comments
            $comments = plugin_callback($this->plugintype, $this->pluginname, 'comment', 'display', array($comments, $this->comment_param), $comments);
        }

        return $comments;
    }