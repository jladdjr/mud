#!/usr/bin/env python3

# storage.py
# abstraction-layer for persisting mud data

from dataclasses import dataclass
from datetime import datetime

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
        self.cache = {}

    def add_file_metadata_snapshot(self, machine: Machine,
                                   dir_path: str,
                                   file_name: str,
                                   scan_time: datetime,
                                   file_size: int,
                                   sha1: str,
                                   created: datetime,
                                   modified: datetime):
        cursor = self.conn.cursor()
        fields = "machine_id, dir_path, file_name, scan_time, file_size, sha1, created, modified"
        value_place_holders = "%s, %s, %s, %s, %s, %s, %s, %s"
        cursor.execute(
            f"INSERT INTO file_metadata_snapshots ({fields}) VALUES ({value_place_holders})",
            (machine.id, dir_path, file_name, scan_time, file_size, sha1, created, modified)
        )
        self.conn.commit()

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
        if "local_machine" in self.cache:
            return self.cache["local_machine"]

        if hostname is None:
            hostname = gethostname()
        machine = self.get_machine(hostname)
        if machine is None:
            machine = self.add_machine(hostname, description)
        self.cache["local_machine"] = machine
        return machine
