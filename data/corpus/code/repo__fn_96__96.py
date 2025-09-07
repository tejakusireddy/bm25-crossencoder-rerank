public static String getNameOfMissingClassLoaderDependency(Throwable e) {
        if (e instanceof NoClassDefFoundError) {
            // NoClassDefFoundError sometimes includes CNFE as the cause. Since CNFE has a better formatted class name
            // and may also include classloader info, we prefer CNFE's over NCDFE's message.
            if (e.getCause() instanceof ClassNotFoundException) {
                return getNameOfMissingClassLoaderDependency(e.getCause());
            }
            if (e.getMessage() != null) {
                return e.getMessage().replace('/', '.');
            }
        }
        if (e instanceof ClassNotFoundException) {
            if (e.getMessage() != null) {
                return e.getMessage();
            }
        }
        if (e.getCause() != null) {
            return getNameOfMissingClassLoaderDependency(e.getCause());
        } else {
            return "[unknown]";
        }
    }