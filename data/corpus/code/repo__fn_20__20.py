static Field lookupField(Class<?> javaClass, String fieldName) throws NoSuchFieldException {
        if (System.getSecurityManager() != null) {
            try {
                return AccessController.doPrivileged(new FieldLookupAction(javaClass, fieldName));
            } catch (PrivilegedActionException e) {
                if (e.getCause() instanceof NoSuchFieldException) {
                    throw (NoSuchFieldException) e.getCause();
                }
                throw new WeldException(e.getCause());
            }
        } else {
            return FieldLookupAction.lookupField(javaClass, fieldName);
        }
    }