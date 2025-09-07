public static String resolveUriPrefix(URI serverURI)
      throws URISyntaxException {
    if (RESTLI_SCHEMES.contains(serverURI.getScheme())) {
      return new URI(serverURI.getScheme(), serverURI.getAuthority(), null, null, null).toString() + "/";
    }

    throw new RuntimeException("Unrecognized scheme for URI " + serverURI);
  }