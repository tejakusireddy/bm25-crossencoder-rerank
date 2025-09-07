public function git($commandString)
    {
        // clean commands that begin with "git "
        $commandString = preg_replace('/^git\s/', '', $commandString);

        $commandString = $this->options['git_executable'].' '.$commandString;

        $command = new $this->options['command_class']($this->dir, $commandString, $this->debug);

        return $command->run();
    }