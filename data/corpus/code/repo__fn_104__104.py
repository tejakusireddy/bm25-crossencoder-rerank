public void setData(String key, String value) {
        QName qn = new QName("data-" + key);
        this.getOtherAttributes().put(qn, value);
    }