public synchronized static <D extends Dao<T, ?>, T> D lookupDao(ConnectionSource connectionSource,
			DatabaseTableConfig<T> tableConfig) {
		if (connectionSource == null) {
			throw new IllegalArgumentException("connectionSource argument cannot be null");
		}
		TableConfigConnectionSource key = new TableConfigConnectionSource(connectionSource, tableConfig);
		Dao<?, ?> dao = lookupDao(key);
		if (dao == null) {
			return null;
		} else {
			@SuppressWarnings("unchecked")
			D castDao = (D) dao;
			return castDao;
		}
	}