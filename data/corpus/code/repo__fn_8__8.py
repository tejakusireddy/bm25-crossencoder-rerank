public TopicProducer<Object> createTopicJsonProducer(final String topic)
    {
        Preconditions.checkState(connectionFactory != null, "connection factory was never injected!");
        return new TopicProducer<Object>(connectionFactory, jmsConfig, topic, producerCallback);
    }