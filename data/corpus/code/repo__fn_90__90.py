def upsert_all(cls, engine, obj_or_data):
        
        cls.update_all(
            engine=engine,
            obj_or_data=obj_or_data,
            upsert=True,
        )