public boolean isCompensationHandler() {
    Boolean isForCompensation = (Boolean) getProperty(BpmnParse.PROPERTYNAME_IS_FOR_COMPENSATION);
    return Boolean.TRUE.equals(isForCompensation);
  }