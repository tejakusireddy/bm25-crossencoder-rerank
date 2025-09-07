def _change_soi(self, body):
        

        if body == self.central:
            self.bodies = [self.central]
            self.step = self.central_step
            self.active = self.central.name
            self.frame = self.central.name
        else:
            soi = self.SOI[body.name]
            self.bodies = [body]
            self.step = self.alt_step
            self.active = body.name
            self.frame = soi.frame