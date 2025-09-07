public FeatureInfoWithActions getFeatureInfoWidgetWithActions(MapPresenter mapPresenter) {
		FeatureInfoWithActions widgetWithActions = new FeatureInfoWithActions();
		widgetWithActions.addHasFeature(new ZoomToObjectAction(mapPresenter));

		return widgetWithActions;
	}