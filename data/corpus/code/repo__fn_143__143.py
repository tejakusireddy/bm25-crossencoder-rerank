def match_files(self, matched, unmatched):
        """"""
        for pattern in self.iter():
            pattern.match_files(matched, unmatched)
            if not unmatched:
                # Optimization: If we have matched all files already
                # simply return at this point - nothing else to do
                break