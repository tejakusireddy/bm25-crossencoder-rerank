public static CollectionReflectionUtilImpl getInstance() {

    if (instance == null) {
      synchronized (CollectionReflectionUtilImpl.class) {
        if (instance == null) {
          CollectionReflectionUtilImpl util = new CollectionReflectionUtilImpl();
          util.initialize();
          instance = util;
        }
      }
    }
    return instance;
  }