public void setRoundedCorners(final boolean ROUNDED) {
        if (null == roundedCorners) {
            _roundedCorners = ROUNDED;
            fireTileEvent(REDRAW_EVENT);
        } else {
            roundedCorners.set(ROUNDED);
        }
    }