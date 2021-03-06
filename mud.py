#!/usr/bin/env python3

import argparse
import configparser
import json
import logging
from pathlib import Path

from psycopg import connect

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATHS=['./.mud', '~/.mud']

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
        return None

def init(args):
    logger.debug('entered init')

    conn = connect(dbname='postgres', user='mud', host='localhost', password='secret')
    cursor = conn.cursor()
    cursor.execute('SHOW WORK_MEM')
    memory = cursor.fetchone()
    print(memory)


def scan(args):
    logger.debug('entered scan')

    config = get_config()
    if config is None or 'scan' not in config or \
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
    parser = argparse.ArgumentParser(description='A multi-machine deduper.')
    subparsers = parser.add_subparsers()

    parser_scan = subparsers.add_parser('scan')
    parser_scan.set_defaults(func=scan)

    parser_scan = subparsers.add_parser('init')
    parser_scan.set_defaults(func=init)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
