#!/usr/bin/env python3

# storage.py
# abstraction-layer for persisting mud data

from dataclasses import dataclass

from psycopg import connect
from socket import gethostname


@dataclass
class Machine:
    id: int
    hostname: str
    description: str


class StorageController:
    def __init__(self, **kwargs):
        supported_kwarg_names = ("host", "dbname", "user", "password")
        supported_kwargs = {}
        for k, v in kwargs.items():
            if k in supported_kwarg_names:
                supported_kwargs[k] = v

        self.conn = connect(**supported_kwargs)

    def add_file_metadata_snapshot(self):
        # TODO create function that looks up machine id based on cache
        pass

    def add_machine(self, hostname, description=""):
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO machines (hostname, description) VALUES (%s, %s) RETURNING machine_id""",
            (hostname, description),
        )
        id = cursor.fetchone()[0]
        self.conn.commit()
        return Machine(id, hostname, description)

    def get_machine(self, hostname):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT machine_id, hostname, description FROM machines WHERE hostname = %s",
            (hostname,),
        )
        res = cursor.fetchone()
        if res is None:
            return None
        id, hostname, description = res
        return Machine(id, hostname, description)

    def get_or_create_machine(self, hostname=None, description=""):
        """Looks up `hostname` machine. If `hostname` is None, searches for machine entry for
        current host. Creates a new Machine entry if none are found. Returns a `Machine` object."""
        if hostname is None:
            hostname = gethostname()
        machine = self.get_machine(hostname)
        if machine:
            return machine
        return self.add_machine(hostname, description)
