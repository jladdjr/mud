#!/usr/bin/env python3

# storage.py
# abstraction-layer for persisting mud data

from psycopg import connect

class StorageController:

    def __init__(self):
        # TODO: Remove hard-coding
        self.conn = connect(dbname='mud', user='mud', host='localhost', password='fixme')

    def store_file_metadata_snapshot(self):
        pass

    def do_something(self):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO machines (machine_id, hostname, description) VALUES (%s, %s, %s)', (1, 'foohost', 'this is the foo host'))
        self.conn.commit()
