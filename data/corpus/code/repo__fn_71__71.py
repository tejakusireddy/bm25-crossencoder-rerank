public static final double bearing(double lat1, double lon1, double lat2, double lon2)
    {
        return Math.toDegrees(radBearing(lat1, lon1, lat2, lon2));
    }