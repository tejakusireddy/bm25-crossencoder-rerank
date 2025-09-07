def _GetMetric(self, metric_name):
    """"""
    if metric_name in self._counter_metrics:
      return self._counter_metrics[metric_name]
    elif metric_name in self._event_metrics:
      return self._event_metrics[metric_name]
    elif metric_name in self._gauge_metrics:
      return self._gauge_metrics[metric_name]
    else:
      raise ValueError("Metric %s is not registered." % metric_name)