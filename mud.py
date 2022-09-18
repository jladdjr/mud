#!/usr/bin/env python3

import argparse
import configparser
import json
import logging
from pathlib import Path

from psycopg import connect

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATHS=['.mud', Path.home() / '.mud']

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

    # Example of how I would connect to the database
    # conn = connect(dbname='postgres', user='mud', host='localhost', password='secret')
    # cursor = conn.cursor()
    # cursor.execute('SHOW WORK_MEM')
    # memory = cursor.fetchone()
    # print(memory)

    # TODO: Prompt user for config info
    mud_path = Path.home() / '.mud'
    with open(mud_path, 'x') as f:
        f.write("""[scan]
scan_dirs = [
    "/home/jim/foo",
    "/home/jim/bar"
    ]
""")

def scan(args):
    logger.debug('entered scan')

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

    for dir in scan_dirs:
        logger.info(f'scanning {dir}')

def main():
    parser = argparse.ArgumentParser(description='A multi-machine file deduper.')
    subparsers = parser.add_subparsers()

    parser_scan = subparsers.add_parser('scan')
    parser_scan.set_defaults(func=scan)

    parser_scan = subparsers.add_parser('init')
    parser_scan.set_defaults(func=init)

    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
    else:
        args.func(args)

if __name__ == '__main__':
    main()
