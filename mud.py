#!/usr/bin/env python3

import argparse
import configparser
from hashlib import sha1
import json
import logging
import os
from pathlib import Path
from time import perf_counter

from storage import StorageController

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATHS = ['.mud', Path.home() / '.mud']


def get_config():
    for path in DEFAULT_CONFIG_PATHS:
        if Path(path).is_file():
            logger.debug(f'Found config file at {path}')
            parser = configparser.ConfigParser()
            parser.read(path)
            return parser
        else:
            logger.debug(f'No config file at {path}')
    else:
        print('Run `mud init` to initiliaze mud')
        return None


def init(args):
    """Initialize the deduper settings"""
    logger.debug('entered init')

    # TODO: Prompt user for config info
    mud_path = Path.home() / '.mud'
    with open(mud_path, 'x') as f:
        f.write("""[scan]
scan_dirs = [
    "/home/jim/foo",
    "/home/jim/bar"
    ]
""")


def test(args):
    sc = StorageController()
    sc.do_something()


def calculate_hash(path):
    """Returns sha1 secure hash / message digest for the file at `path`"""
    t1 = perf_counter()
    s = sha1()
    with open(path, 'rb') as f:
        s.update(f.read())
    t2 = perf_counter()
    elapsed_in_ms = (t2 - t1) * 1000
    logger.debug(f'Hashed {path} in {elapsed_in_ms:.3f} ms')
    return s.hexdigest()


def scan(args):
    # sc = StorageController()

    logger.debug('entered scan')
    t1 = perf_counter()

    config = get_config()
    if config is None:
        # missing config file, exit
        return
    if 'scan' not in config or \
            'scan_dirs' not in config['scan']:
        logger.info('scan directories not defined in config file')
        return

    scan_dirs = json.loads(config['scan']['scan_dirs'])
    if len(scan_dirs) == 0:
        logger.debug('scan_dirs empty')
        return

    num_scanned_files = 0
    for dir in scan_dirs:
        logger.debug(f'Scanning      {dir}')
        for root, dirs, files in os.walk(dir):
            logger.debug(f'Visiting:     {root}')
            logger.debug(f'Dirs:         {dirs}')
            logger.debug(f'Files:        {files}')

            for f in files:
                p = os.path.join(root, f)
                hash = calculate_hash(p)
                logger.debug(f'{f} hash: {hash}')

                # save hash data

            num_scanned_files += len(files)

    t2 = perf_counter()
    elapsed_in_ms = (t2 - t1)
    logger.debug(f'Scanned {num_scanned_files} files in {elapsed_in_ms:.3f} seconds')


def main():
    parser = argparse.ArgumentParser(description='A multi-machine file deduper.')
    subparsers = parser.add_subparsers()

    parser_scan = subparsers.add_parser('scan')
    parser_scan.set_defaults(func=scan)

    parser_scan = subparsers.add_parser('init')
    parser_scan.set_defaults(func=init)

    parser_scan = subparsers.add_parser('test')
    parser_scan.set_defaults(func=test)

    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
    else:
        args.func(args)


if __name__ == '__main__':
    main()
