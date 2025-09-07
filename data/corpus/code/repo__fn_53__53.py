def add_arguments(self, parser):
        """"""
        parser.add_argument(self._source_param, **self._source_kwargs)
        parser.add_argument('--base', '-b', action='store',
            help=   'Supply the base currency as code or a settings variable name. '
                    'The default is taken from settings CURRENCIES_BASE or SHOP_DEFAULT_CURRENCY, '
                    'or the db, otherwise USD')