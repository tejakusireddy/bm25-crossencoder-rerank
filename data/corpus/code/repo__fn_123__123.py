func (s *Schema) refToSchema(str string, rootSchema Schema, loadExternal bool) (*Schema, error) {
	parentURL, err := url.Parse(s.parentId)
	if err == nil && parentURL.IsAbs() {
		sURL, err := url.Parse(str)
		if err == nil && !sURL.IsAbs() && !strings.HasPrefix(str, "#") {
			str = parentURL.ResolveReference(sURL).String()
		}
	}

	var split []string
	url, err := url.Parse(str)
	cacheKey, cacheKeyErr := resolveCacheKey(str)
	if err == nil && cacheKeyErr == nil {
		cachedSchema, ok := rootSchema.Cache[cacheKey]
		if ok {
			rootSchema = *cachedSchema
		} else {
			// Handle external URIs.
			if !loadExternal {
				return new(Schema), errors.New("external schemas are disabled")
			}
			resp, err := http.Get(str)
			if err != nil {
				return new(Schema), errors.New("bad external url")
			}
			defer resp.Body.Close()
			s, err := ParseWithCache(resp.Body, loadExternal, &rootSchema.Cache)
			if err != nil {
				return new(Schema), errors.New("error parsing external doc")
			}
			rootSchema.Cache[cacheKey] = s
			rootSchema = *s
		}
		str = url.Fragment
	}

	// Remove the prefix from internal URIs.
	str = strings.TrimPrefix(str, "#")
	str = strings.TrimPrefix(str, "/")

	split = strings.Split(str, "/")
	// Make replacements.
	for i, v := range split {
		r := strings.NewReplacer("~0", "~", "~1", "/", "%25", "%")
		split[i] = r.Replace(v)
	}
	// Resolve the local part of the URI.
	return resolveLocalPath(split, rootSchema, str)
}