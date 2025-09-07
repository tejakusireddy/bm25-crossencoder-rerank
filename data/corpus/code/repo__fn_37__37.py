func (s *Service) Run() {
	flag.Usage = s.Usage
	flag.Parse()
	args := flag.Args()
	if len(args) == 0 && s.defaultCommand != "" {
		args = append([]string{s.defaultCommand}, args...)
	}
	if len(args) == 0 {
		s.Usage()
		BootPrintln()
		return
	}
	err := s.RunCommand(args[0], args[1:]...)
	if err != nil {
		panic(err)
	}
}