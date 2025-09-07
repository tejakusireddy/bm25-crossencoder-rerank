public static String getTerminRoot(Long channelId, Long pipelineId) {
        // 根据channelId , pipelineId构造path
        return MessageFormat.format(ArbitrateConstants.NODE_TERMIN_ROOT,
            String.valueOf(channelId),
            String.valueOf(pipelineId));
    }