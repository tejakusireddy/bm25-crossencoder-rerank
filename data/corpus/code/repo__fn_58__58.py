func (co *Coordinator) StartPlugins() {
	// Launch routers
	for _, router := range co.routers {
		logrus.Debug("Starting ", reflect.TypeOf(router))
		if err := router.Start(); err != nil {
			logrus.WithError(err).Errorf("Failed to start router of type '%s'", reflect.TypeOf(router))
		}
	}

	// Launch producers
	co.state = coordinatorStateStartProducers
	for _, producer := range co.producers {
		producer := producer
		go tgo.WithRecoverShutdown(func() {
			logrus.Debug("Starting ", reflect.TypeOf(producer))
			producer.Produce(co.producerWorker)
		})
	}

	// Set final log target and purge the intermediate buffer
	if core.StreamRegistry.IsStreamRegistered(core.LogInternalStreamID) {
		// The _GOLLUM_ stream has listeners, so use LogConsumer to write to it
		if *flagLogColors == "always" {
			logrus.SetFormatter(logger.NewConsoleFormatter())
		}
		logrusHookBuffer.SetTargetHook(co.logConsumer)
		logrusHookBuffer.Purge()

	} else {
		logrusHookBuffer.SetTargetWriter(logger.FallbackLogDevice)
		logrusHookBuffer.Purge()
	}

	// Launch consumers
	co.state = coordinatorStateStartConsumers
	for _, consumer := range co.consumers {
		consumer := consumer
		go tgo.WithRecoverShutdown(func() {
			logrus.Debug("Starting ", reflect.TypeOf(consumer))
			consumer.Consume(co.consumerWorker)
		})
	}
}