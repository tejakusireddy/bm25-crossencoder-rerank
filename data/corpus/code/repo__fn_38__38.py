def _put_one(self, item):
        ''' 
        '''
        # prepare values
        values = []
        for k, v in item.items():
            if k == '_id':
                continue
            if 'dblite_serializer' in item.fields[k]:
                serializer = item.fields[k]['dblite_serializer']
                v = serializer.dumps(v)
                if v is not None:
                    v = sqlite3.Binary(buffer(v))
            values.append(v)

        # check if Item is new => update it
        if '_id' in item:
            fieldnames = ','.join(['%s=?' % f for f in item if f != '_id'])
            values.append(item['_id'])
            SQL = 'UPDATE %s SET %s WHERE rowid=?;' % (self._table, fieldnames)
        # new Item
        else:
            fieldnames = ','.join([f for f in item if f != '_id'])
            fieldnames_template = ','.join(['?' for f in item if f != '_id'])
            SQL = 'INSERT INTO %s (%s) VALUES (%s);' % (self._table, fieldnames, fieldnames_template)

        try:
            self._cursor.execute(SQL, values)
        except sqlite3.OperationalError, err:
            raise RuntimeError('Item put() error, %s, SQL: %s, values: %s' % (err, SQL, values) )
        except sqlite3.IntegrityError:
            raise DuplicateItem('Duplicate item, %s' % item)
        self._do_autocommit()