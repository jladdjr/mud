#!/usr/bin/env python3

# storage.py
# abstraction-layer for persisting mud data

from psycopg import connect

class StorageController:

    def __init__(self, **kwargs):
        supported_kwarg_names = ('host', 'dbname', 'user', 'password')
        supported_kwargs = {}
        for k, v in kwargs.items():
            if k in supported_kwarg_names:
                supported_kwargs[k] = v

        self.conn = connect(**supported_kwargs)

    def add_file_metadata_snapshot(self):
        pass

    def add_machine(self, hostname, description):
        cursor = self.conn.cursor()
        cursor.execute("""INSERT INTO machines (hostname, description) VALUES (%s, %s)""",
                       (hostname, description))
        self.conn.commit()

    def get_machine(self, hostname):
        cursor = self.conn.cursor()
        cursor.execute("SELECT hostname, description from machines where hostname = %s", (hostname,))
        return cursor.fetchone()
