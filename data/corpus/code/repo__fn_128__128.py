func (c *command) connect() error {
	if c.connected {
		return transport.ErrAlreadyConnected
	}

	if c.auth == nil {
		if err := c.setAuthFromEndpoint(); err != nil {
			return err
		}
	}

	var err error
	config, err := c.auth.ClientConfig()
	if err != nil {
		return err
	}

	overrideConfig(c.config, config)

	c.client, err = dial("tcp", c.getHostWithPort(), config)
	if err != nil {
		return err
	}

	c.Session, err = c.client.NewSession()
	if err != nil {
		_ = c.client.Close()
		return err
	}

	c.connected = true
	return nil
}