private function _write_log($daily = false, $hourly = false, $backtrace = false) {

        // if we are using a callback function to handle logs
        if (is_callable($this->log_path) && !isset($this->log_path_is_function))

            // set flag
            $this->log_path_is_function = true;

        // if we are writing logs to a file
        else {

            // set flag
            $this->log_path_is_function = false;

            $pathinfo = pathinfo($this->log_path);

            // if log_path is given as full path to a file, together with extension
            if (isset($pathinfo['filename']) && isset($pathinfo['extension'])) {

                // use those values
                $file_name = $pathinfo['dirname'] . '/' . $pathinfo['filename'];
                $extension = '.' . $pathinfo['extension'];

            // otherwise
            } else {

                // the file name is "log" and the extension is ".txt"
                $file_name = rtrim($this->log_path, '/\\') . '/log';
                $extension = '.txt';

            }

            // if $hourly is set to TRUE, $daily *must* be true
            if ($hourly) $daily = true;

            // are we writing daily logs?
            // (suppress "strict standards" warning for PHP 5.4+)
            $file_name .= ($daily ? '-' . @date('Ymd') : '');

            // are we writing hourly logs?
            // (suppress "strict standards" warning for PHP 5.4+)
            $file_name .= ($hourly ? '-' . @date('H') : '');

            // log file's extension
            $file_name .= $extension;

        }

        // all the labels that may be used in a log entry
        $labels = array(
            strtoupper($this->language['date']),
            strtoupper('query'),
            strtoupper($this->language['execution_time']),
            strtoupper($this->language['warning']),
            strtoupper($this->language['error']),
            strtoupper($this->language['from_cache']),
            strtoupper($this->language['yes']),
            strtoupper($this->language['no']),
            strtoupper($this->language['backtrace']),
            strtoupper($this->language['file']),
            strtoupper($this->language['line']),
            strtoupper($this->language['function']),
            strtoupper($this->language['unbuffered']),
        );

        // determine the longest label (for proper indenting)
        $longest_label_length = 0;

        // iterate through the labels
        foreach ($labels as $label)

            // if the label is longer than the longest label so far
            if (strlen($label) > $longest_label_length)

                // this is the longes label, so far
                // we use utf8_decode so that strlen counts correctly with accented chars
                $longest_label_length = strlen(utf8_decode($label));

        $longest_label_length--;

        // the following regular expressions strips newlines and indenting from the MySQL string, so that
        // we have it in a single line
        $pattern = array(
            "/\s*(.*)\n|\r/",
            "/\n|\r/"
        );

        $replace = array(
            ' $1',
            ' '
        );

        // if we are using a callback function for logs or we are writing the logs to a file and we can create/write to the log file
        if ($this->log_path_is_function || $handle = @fopen($file_name, 'a+')) {

            // we need to show both successful and unsuccessful queries
            $sections = array('successful-queries', 'unsuccessful-queries');

            // iterate over the sections we need to show
            foreach ($sections as $section) {

                // if there are any queries in the section
                if (isset($this->debug_info[$section])) {

                    // iterate through the debug information
                    foreach ($this->debug_info[$section] as $debug_info) {

                        // the output
                        $output =

                            // date
                            $labels[0] . str_pad('', $longest_label_length - strlen(utf8_decode($labels[0])), ' ', STR_PAD_RIGHT) . ': ' . @date('Y-m-d H:i:s') . "\n" .

                            // query
                            $labels[1] . str_pad('', $longest_label_length - strlen(utf8_decode($labels[1])), ' ', STR_PAD_RIGHT) . ': ' . trim(preg_replace($pattern, $replace, $debug_info['query'])) . "\n" .

                            // if execution time is available
                            // (is not available for unsuccessful queries)
                            (isset($debug_info['execution_time']) ? $labels[2] . str_pad('', $longest_label_length - strlen(utf8_decode($labels[2])), ' ', STR_PAD_RIGHT) . ': ' . $this->_fix_pow($debug_info['execution_time']) . ' ' . $this->language['seconds'] . "\n" : '') .

                            // if there is a warning message
                            (isset($debug_info['warning']) && $debug_info['warning'] != '' ? $labels[3] . str_pad('', $longest_label_length - strlen(utf8_decode($labels[3])), ' ', STR_PAD_RIGHT) . ': ' . strip_tags($debug_info['warning']) . "\n" : '') .

                            // if there is an error message
                            (isset($debug_info['error']) && $debug_info['error'] != '' ? $labels[4] . str_pad('', $longest_label_length - strlen(utf8_decode($labels[4])), ' ', STR_PAD_RIGHT) . ': ' . $debug_info['error'] . "\n" : '') .

                            // if not an action query, show whether the query was returned from the cache or was executed
                            (isset($debug_info['affected_rows']) && $debug_info['affected_rows'] === false && isset($debug_info['from_cache']) && $debug_info['from_cache'] != 'nocache' ? $labels[5] . str_pad('', $longest_label_length - strlen(utf8_decode($labels[5])), ' ', STR_PAD_RIGHT) . ': ' . $labels[6] . "\n" : '') .

                            // if query was an unbuffered one
                            (isset($debug_info['unbuffered']) && $debug_info['unbuffered'] ? $labels[12] . str_pad('', $longest_label_length - strlen(utf8_decode($labels[12])), ' ', STR_PAD_RIGHT) . ': ' . $labels[6] . "\n" : '');

                        // if we are writing the logs to a file, write to the log file
                        if (!$this->log_path_is_function) fwrite($handle, print_r($output, true));

                        $backtrace_output = '';

                        // if backtrace information should be written to the log file
                        if ($backtrace) {

                            $backtrace_output = $labels[8] . str_pad('', $longest_label_length - strlen(utf8_decode($labels[8])), ' ', STR_PAD_RIGHT) . ':' . "\n";

                            // if we are writing the logs to a file, write to the log file
                            if (!$this->log_path_is_function) fwrite($handle, print_r($backtrace_output, true));

                            // handle full backtrace info
                            foreach ($debug_info['backtrace'] as $backtrace) {

                                // output
                                $tmp =
                                    "\n" .
                                    $labels[9] . str_pad('', $longest_label_length - strlen(utf8_decode($labels[9])), ' ', STR_PAD_RIGHT) . ': ' . $backtrace[$this->language['file']] . "\n" .
                                    $labels[10] . str_pad('', $longest_label_length - strlen(utf8_decode($labels[10])), ' ', STR_PAD_RIGHT) . ': ' . $backtrace[$this->language['line']] . "\n" .
                                    $labels[11] . str_pad('', $longest_label_length - strlen(utf8_decode($labels[11])), ' ', STR_PAD_RIGHT) . ': ' . $backtrace[$this->language['function']] . "\n";

                                // if we are writing the logs to a file, write to the log file
                                if (!$this->log_path_is_function) fwrite($handle, print_r($tmp, true));

                                // otherwise, add to the string
                                else $backtrace_output .= $tmp;

                            }

                        }

                        // if we are writing the logs to a file, finish writing to the log file by adding a bottom border
                        if (!$this->log_path_is_function) fwrite($handle, str_pad('', $longest_label_length + 1, '-', STR_PAD_RIGHT) . "\n");

                        // if we are using a callback to manage logs, pass log information to the log file
                        else call_user_func_array($this->log_path, array($output, $backtrace_output));

                    }

                }

            }

            // if we are writing the logs to a file, close the log file
            if (!$this->log_path_is_function) fclose($handle);

        // if log file could not be created/opened
        } else

            trigger_error($this->language['could_not_write_to_log'], E_USER_ERROR);

    }