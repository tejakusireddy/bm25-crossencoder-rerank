public void clearKSMap() {
        if (TraceComponent.isAnyTracingEnabled() && tc.isDebugEnabled())
            Tr.debug(tc, "Clearing keystore maps");
        synchronized (keyStoreMap) {
            keyStoreMap.clear();
        }
    }