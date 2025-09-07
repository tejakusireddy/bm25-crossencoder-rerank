def end(self, close_fileobj=True):
        """"""
        log.debug("in TftpContext.end - closing socket")
        self.sock.close()
        if close_fileobj and self.fileobj is not None and not self.fileobj.closed:
            log.debug("self.fileobj is open - closing")
            self.fileobj.close()