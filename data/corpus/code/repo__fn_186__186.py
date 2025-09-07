func ParseToRawMap(fileName string) (cfg RawMap, err error) {
	var file *os.File

	cfg = make(RawMap, 0)
	file, err = os.Open(fileName)
	if err != nil {
		return
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)

	var currentSection string
	for scanner.Scan() {
		line := scanner.Text()

		if commentLine.MatchString(line) {
			continue
		} else if blankLine.MatchString(line) {
			continue
		} else if configSection.MatchString(line) {
			section := configSection.ReplaceAllString(line, "$1")
			if !cfg.SectionInConfig(section) {
				cfg[section] = make(map[string]string, 0)
			}
			currentSection = section
		} else if configLine.MatchString(line) {
			regex := configLine
			if quotedConfigLine.MatchString(line) {
				regex = quotedConfigLine
			}
			if currentSection == "" {
				currentSection = defaultSection
				if !cfg.SectionInConfig(currentSection) {
					cfg[currentSection] = make(map[string]string, 0)
				}
			}
			key := regex.ReplaceAllString(line, "$1")
			val := regex.ReplaceAllString(line, "$2")
			cfg[currentSection][key] = val
		} else {
			err = fmt.Errorf("invalid config file")
			break
		}
	}
	return
}