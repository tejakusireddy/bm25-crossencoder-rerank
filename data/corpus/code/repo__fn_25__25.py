public void submit(String name, Map<String, String> additionalMetadata) {
    if(this.metricContext.isPresent()) {
      Map<String, String> finalMetadata = Maps.newHashMap(this.metadata);
      if(!additionalMetadata.isEmpty()) {
        finalMetadata.putAll(additionalMetadata);
      }

      // Timestamp is set by metric context.
      this.metricContext.get().submitEvent(new GobblinTrackingEvent(0l, this.namespace, name, finalMetadata));
    }
  }