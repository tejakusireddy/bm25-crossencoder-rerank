public static String[] trimAll(final String[] strings) {
        if (null == strings) {
            return null;
        }

        return Arrays.stream(strings).map(StringUtils::trim).toArray(size -> new String[size]);
    }