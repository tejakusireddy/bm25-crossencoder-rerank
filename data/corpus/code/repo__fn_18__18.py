public void setUrl(final String url) {
		MenuItemModel model = getOrCreateComponentModel();
		model.url = url;
		model.action = null;
	}