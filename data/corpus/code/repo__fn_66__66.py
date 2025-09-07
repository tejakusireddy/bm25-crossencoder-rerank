public OrderItem withPromotionIds(String... values) {
        List<String> list = getPromotionIds();
        for (String value : values) {
            list.add(value);
        }
        return this;
    }