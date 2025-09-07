def monitor(self):
        
        if self._monitor is None:
            from twilio.rest.monitor import Monitor
            self._monitor = Monitor(self)
        return self._monitor