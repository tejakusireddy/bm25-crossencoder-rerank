@Override
	public void configure(Configuration parameters) {

		// enforce sequential configuration() calls
		synchronized (CONFIGURE_MUTEX) {
			if (mapreduceInputFormat instanceof Configurable) {
				((Configurable) mapreduceInputFormat).setConf(configuration);
			}
		}
	}