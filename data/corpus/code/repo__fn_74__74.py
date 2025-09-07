public SyntacticCategory assignAllFeatures(String value) {
    Set<Integer> featureVars = Sets.newHashSet();
    getAllFeatureVariables(featureVars);

    Map<Integer, String> valueMap = Maps.newHashMap();
    for (Integer var : featureVars) {
      valueMap.put(var, value);
    }
    return assignFeatures(valueMap, Collections.<Integer, Integer>emptyMap());
  }