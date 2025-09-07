public static String getParamFromState(String state, String paramName) {

        String prefix = PARAM_SEPARATOR + paramName + PARAM_ASSIGN;
        if (state.contains(prefix)) {
            String result = state.substring(state.indexOf(prefix) + prefix.length());
            if (result.contains(PARAM_SEPARATOR)) {
                result = result.substring(0, result.indexOf(PARAM_SEPARATOR));
            }
            return CmsEncoder.decode(result, CmsEncoder.ENCODING_UTF_8);
        }
        return null;
    }