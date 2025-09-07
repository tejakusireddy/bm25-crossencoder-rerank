protected function generateLicense()
    {
        $command = $this->prepareSignCommand() . ' 2>&1';

        $this->log('Creating license at ' . $this->outputFile);

        $this->log('Running: ' . $command, Project::MSG_VERBOSE);
        $tmp = exec($command, $output, $return_var);

        // Check for exit value 1. Zendenc_sign command for some reason
        // returns 0 in case of failure and 1 in case of success...
        if ($return_var !== 1) {
            throw new BuildException("Creating license failed. \n\nZendenc_sign msg:\n" . implode(
                "\n",
                $output
            ) . "\n\n");
        }
    }