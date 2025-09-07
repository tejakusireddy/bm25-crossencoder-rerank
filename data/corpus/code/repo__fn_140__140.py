final public String getFullName(final String parent) {
    if (isEmptyLocalName()) {
      return parent;
    }
    
    StringBuilder fullName = new StringBuilder(parent);
    if (!parent.endsWith(Path.SEPARATOR)) {
      fullName.append(Path.SEPARATOR);
    }
    fullName.append(getLocalName());
    return fullName.toString();
  }