#!/usr/bin/env python3

import unittest
from datetime import datetime, timedelta
from unittest import mock

from storage import StorageController, Machine


class StorageControllerTests(unittest.TestCase):
    @mock.patch("storage.connect")
    def test_add_machine(self, connect_mock):
        sc = StorageController()
        sc.add_machine("foo_machine", "this is the foo machine")
        expected_execute_args = (
            "INSERT INTO machines (hostname, description) VALUES (%s, %s) RETURNING machine_id",
            ("foo_machine", "this is the foo machine"),
        )
        execute_mock = connect_mock.return_value.cursor.return_value.execute
        execute_mock.assert_called_once_with(*expected_execute_args)

    @mock.patch("storage.connect")
    def test_get_machine(self, connect_mock):
        cursor_mock = connect_mock.return_value.cursor.return_value
        cursor_mock.fetchone.return_value = (1, "foo_machine", "my foo machine")

        sc = StorageController()
        m = sc.get_machine("foo_machine")
        expected_execute_args = (
            "SELECT machine_id, hostname, description FROM machines WHERE hostname = %s",
            ("foo_machine",),
        )
        execute_mock = connect_mock.return_value.cursor.return_value.execute
        execute_mock.assert_called_once_with(*expected_execute_args)
        self.assertEqual(m.id, 1)
        self.assertEqual(m.hostname, "foo_machine")
        self.assertEqual(m.description, "my foo machine")

    @mock.patch("storage.gethostname")
    @mock.patch("storage.StorageController.get_machine")
    @mock.patch("storage.connect")
    def test_get_or_create_machine(
        self, mock_connect, get_machine_mock, gethostname_mock
    ):
        gethostname_mock.return_value = "enigma"
        this_machine = Machine(1, "enigma", "the enigma machine")
        get_machine_mock.return_value = this_machine

        sc = StorageController()
        m = sc.get_or_create_machine()
        self.assertEqual(m, this_machine)

    @mock.patch("storage.connect")
    def test_add_file_metadata_snapshot(self, connect_mock):
        sc = StorageController()
        scan_time = datetime.now()
        created = datetime.now() - timedelta(days=30)
        modified = datetime.now() - timedelta(days=15)
        machine = Machine(1379, "enigma", "the enigma machine")
        sc.add_file_metadata_snapshot(
            machine=machine,
            dir_path="/some/path",
            file_name="foo",
            scan_time=scan_time,
            file_size=4222242,
            sha1="78b371f0ea1410abc62ccb9b7f40c34288a72e1a",
            created=created,
            modified=modified,
        )

        execute_mock = connect_mock.return_value.cursor.return_value.execute
        insert_fields = "machine_id, dir_path, file_name, scan_time, file_size, sha1, created, modified"
        value_place_holders = "%s, %s, %s, %s, %s, %s, %s, %s"
        expected_execute_args = (
            f"INSERT INTO file_metadata_snapshots ({insert_fields}) VALUES ({value_place_holders})",
            (
                1379,
                "/some/path",
                "foo",
                scan_time,
                4222242,
                "78b371f0ea1410abc62ccb9b7f40c34288a72e1a",
                created,
                modified,
            ),
        )
        execute_mock.assert_called_once_with(*expected_execute_args)
