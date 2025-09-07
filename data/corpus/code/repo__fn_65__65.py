public static Object extract(final DeviceAttribute da) throws DevFailed {
	if (da == null) {
		throw DevFailedUtils.newDevFailed(ERROR_MSG_DA);
	}
	return InsertExtractFactory.getAttributeExtractor(da.getType()).extract(da);
    }