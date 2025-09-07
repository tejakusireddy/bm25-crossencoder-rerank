def prod(self, **kwargs):
        
        if self._is_transposed:
            kwargs["axis"] = kwargs.get("axis", 0) ^ 1
            return self.transpose().prod(**kwargs)
        return self._process_sum_prod(
            self._build_mapreduce_func(pandas.DataFrame.prod, **kwargs), **kwargs
        )