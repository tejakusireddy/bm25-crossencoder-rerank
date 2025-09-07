def validate(self):
    """"""
    # PASS if all our validators return True, otherwise FAIL.
    try:
      if all(v(self.measured_value.value) for v in self.validators):
        self.outcome = Outcome.PASS
      else:
        self.outcome = Outcome.FAIL
      return self
    except Exception as e:  # pylint: disable=bare-except
      _LOG.error('Validation for measurement %s raised an exception %s.',
                 self.name, e)
      self.outcome = Outcome.FAIL
      raise
    finally:
      if self._cached:
        self._cached['outcome'] = self.outcome.name