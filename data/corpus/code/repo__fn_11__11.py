protected function getControlKey($disconnect = false)
    {
        $key = '';

        if ($disconnect) {
            return "*immed";
        }

        /*
        if(?) *justproc
        if(?) *debug
        if(?) *debugproc
        if(?) *nostart
        if(?) *rpt*/

        // Idle timeout supported by XMLSERVICE 1.62
        // setting idle for *sbmjob protects the time taken by program calls
        // Do that with *idle(30/kill) or whatever the time in seconds.
        if (trim($this->getOption('idleTimeout')) != '') {
            $idleTimeout = $this->getOption('idleTimeout');
            $key .= " *idle($idleTimeout/kill)"; // ends idle only, but could end MSGW with *call(30/kill)
        }

        // if cdata requested, request it. XMLSERVICE will then wrap all output in CDATA tags.
        if ($this->getOption('cdata')) {
            $key .= " *cdata";
        }

        /* stateless calls in stored procedure job
         *
         * Add *here, which will run everything inside the current PHP/transport job
         * without spawning or submitting a separate XTOOLKIT job.
         */
        if ($this->isStateless()) {
            $key .= " *here";
        } else {
            // not stateless, so could make sense to supply *sbmjob parameters for spawning a separate job.
            if (trim($this->getOption('sbmjobParams')) != '') {
               $sbmjobParams = $this->getOption('sbmjobParams');
               $key .= " *sbmjob($sbmjobParams)";
            }
        }

        // if internal XMLSERVICE tracing, into database table XMLSERVLOG/LOG, is desired
        if ($this->getOption('trace')) {
            $key .= " *log";
        }

        // directive not to run any program, but to parse XML and return parsed output, including dim/dou.
        if ($this->getOption('parseOnly')) {
            $key .= " *test";

            // add a debugging level (1-9) to the parse, to make *test(n) where n is the debugging level
            if ($parseDebugLevel = $this->getOption('parseDebugLevel')) {
                $key .= "($parseDebugLevel)";
            }
        }

        // return XMLSERVICE version/license information (no XML calls)
        if ($this->getOption('license')) {
            $key .= " *license";
        }

        // check proc call speed (no XML calls)
        if ($this->getOption('transport')) {
            $key .= " *justproc";
        }

        // get performance of last call data (no XML calls)
        if ($this->getOption('performance')) {
            $key .= " *rpt";
        }

        // *fly is number of ticks of each operation. *nofly is the default
        if ($this->getOption('timeReport')) {
            $key .= " *fly";
        }

        // PASE CCSID for <sh> type of functions such as WRKACTJOB ('system' command in PASE)
        if ($paseCcsid = $this->getOption('paseCcsid')) {
            $key .= " *pase($paseCcsid)";
        }

        // allow custom control keys
        if ($this->getOption('customControl')) {
            $key .= " {$this->getOption('customControl')}";
        }

        return trim($key); // trim off any extra blanks on beginning or end
    }