#!/usr/bin/env python3

import argparse
import configparser
import json
import logging
import os
from datetime import datetime
from pathlib import Path

from storage import StorageController
from utils import calculate_hash, get_hostname

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATHS = [".mudrc", Path.home() / ".mudrc"]


def get_config():
    for path in DEFAULT_CONFIG_PATHS:
        if Path(path).is_file():
            logger.debug(f"Found config file at {path}")
            parser = configparser.ConfigParser()
            parser.read(path)
            return parser
        else:
            logger.debug(f"No config file at {path}")
    else:
        print("Run `mud init` to initiliaze mud")
        return None


def collect_db_config(config):
    if 'db' not in config.sections():
        raise DB_Config_Missing()
    db_options = ('host', 'dbname', 'user', 'password')
    db_config = {}
    for item in config['db'].items():
        key, value = item
        if key not in db_options:
            logger.warning(f"'{key}' not a valid entry in [db] section of config")
            continue
        db_config[key] = value.replace('"', '')
    return db_config


STORAGE_CONTROLLER = None


def get_storage_controller(db_config):
    global STORAGE_CONTROLLER
    if not STORAGE_CONTROLLER:
        STORAGE_CONTROLLER = StorageController(**db_config)
    return STORAGE_CONTROLLER


def register_machine(args):
    sc = get_storage_controller(collect_db_config(get_config()))
    logger.debug("Registering this machine")

    # TODO: Add support for letting user specify description for the machine
    hostname = get_hostname()
    if sc.get_machine(hostname):
        print(f"{hostname} already registered!")
        return
    sc.add_machine(hostname, "TODO: Add support for description")
    logger.debug(f"Registered {hostname}")
    print(f"Registered {hostname}")


def get_machine_id():
    sc = get_storage_controller(collect_db_config(get_config()))
    this_machine = sc.get_machine()
    return this_machine.id


def init(args):
    """Initialize the deduper settings"""
    logger.debug("entered init")

    # TODO: Prompt user for config info
    mud_path = Path.home() / ".mudrc"
    with open(mud_path, "x") as f:
        f.write(
            """[scan]
scan_dirs = [
    "/home/jim/foo",
    "/home/jim/bar"
    ]

[db]
host = localhost
dbname = mud
user = mud
password = fixme
"""
        )

def is_regular_file(path, filename):
    p = os.path.join(path, filename)
    return os.path.isfile(p)


def is_symbolic_link(path, filename):
    p = os.path.join(path, filename)
    return os.path.islink(p)


def collect_file_metadata(path, filename):
    p = os.path.join(path, filename)
    hash = calculate_hash(p)
    file_stat = os.lstat(p)
    size = file_stat.st_size
    created = datetime.fromtimestamp(file_stat.st_ctime)
    modified = datetime.fromtimestamp(file_stat.st_mtime)

    return { 'dir_path': path,
             'file_name': filename,
             'file_size': size,
             'sha1': hash,
             'created': created,
             'modified': modified }


class DB_Config_Missing(Exception):
    pass


def scan(args):
    config = get_config()
    sc = get_storage_controller(collect_db_config(config))
    machine_id = get_machine_id()

    logger.debug("entered scan")
    t1 = perf_counter()

    if config is None:
        # missing config file, exit
        return
    if "scan" not in config or "scan_dirs" not in config["scan"]:
        logger.info("scan directories not defined in config file")
        return

    scan_dirs = json.loads(config["scan"]["scan_dirs"])
    if len(scan_dirs) == 0:
        logger.debug("scan_dirs empty")
        return

    # TODO: Count number of files to visit before beginning to collect data?
    # TODO: Surface this as progress bar?
    num_scanned_files = 0
    for dir in scan_dirs:
        logger.debug(f"Scanning      {dir}")
        for root, dirs, files in os.walk(dir):
            logger.debug(f"Visiting:     {root}")
            logger.debug(f"Dirs:         {dirs}")
            logger.debug(f"Files:        {files}")

            for f in files:
                if not is_regular_file(root, f):
                    logger.debug(f"Skipping {f} (not regular file)")
                    continue

                metadata = { 'machine_id': machine_id,
                             'scan_time': datetime.now() }
                metadata.update(collect_file_metadata(root, f))
                # TODO: Skip file if hasn't changed since last scan time
                # TODO: Create add_or_update_file_metadata_snapshot?
                sc.add_file_metadata_snapshot(**metadata)

            num_scanned_files += len(files)

    t2 = perf_counter()
    elapsed_in_ms = t2 - t1
    logger.debug(f"Scanned {num_scanned_files} files in {elapsed_in_ms:.3f} seconds")


def main():
    parser = argparse.ArgumentParser(description="A multi-machine file deduper.")
    subparsers = parser.add_subparsers()

    parser_scan = subparsers.add_parser("init")
    parser_scan.set_defaults(func=init)

    parser_scan = subparsers.add_parser("scan")
    parser_scan.set_defaults(func=scan)

    parser_scan = subparsers.add_parser("register_machine")
    parser_scan.set_defaults(func=register_machine)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    main()
