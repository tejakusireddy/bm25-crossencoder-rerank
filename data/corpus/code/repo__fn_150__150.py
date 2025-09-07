@Override
  public List<ExecutableFlow> getRunningFlows() {
    final ArrayList<ExecutableFlow> flows = new ArrayList<>();
    try {
      getFlowsHelper(flows, this.executorLoader.fetchUnfinishedFlows().values());
    } catch (final ExecutorManagerException e) {
      logger.error("Failed to get running flows.", e);
    }
    return flows;
  }