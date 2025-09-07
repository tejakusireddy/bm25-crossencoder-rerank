public void marshall(MethodSnapshot methodSnapshot, ProtocolMarshaller protocolMarshaller) {

        if (methodSnapshot == null) {
            throw new SdkClientException("Invalid argument passed to marshall(...)");
        }

        try {
            protocolMarshaller.marshall(methodSnapshot.getAuthorizationType(), AUTHORIZATIONTYPE_BINDING);
            protocolMarshaller.marshall(methodSnapshot.getApiKeyRequired(), APIKEYREQUIRED_BINDING);
        } catch (Exception e) {
            throw new SdkClientException("Unable to marshall request to JSON: " + e.getMessage(), e);
        }
    }