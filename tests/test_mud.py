#!/usr/bin/env python3

import unittest
from unittest import mock

from storage import StorageController

class StorageControllerTests(unittest.TestCase):


    @mock.patch('storage.connect')
    def test_add_machine(self, connect_mock):
        sc = StorageController()
        sc.add_machine('foo_machine', 'this is the foo machine')
        expected_execute_args = ('INSERT INTO machines (hostname, description) VALUES (%s, %s)',
                                 ('foo_machine', 'this is the foo machine'))
        execute_mock = connect_mock.return_value.cursor.return_value.execute
        execute_mock.assert_called_once_with(*expected_execute_args)
