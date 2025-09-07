def add_migrations(self, migrations):
        
        if self.__closed:
            raise MigrationSessionError("Can't change applied session")
        self._to_apply.extend(migrations)