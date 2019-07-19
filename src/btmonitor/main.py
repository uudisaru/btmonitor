# -*- coding: utf-8 -*-

"""Console script for btmonitor."""
from btmonitor.app import run
from btmonitor.auth.jwt_auth import create_token
from btmonitor.config import setup_logging

import click
import logging


@click.group()
def main():
    """Bus traffic monitor commands"""
    pass


@main.command()
@click.option('-l', '--logging-conf', default='logging.ini')
@click.option('-h', '--host', default='0.0.0.0')
@click.option('-p', '--port', default=8000)
def server(logging_conf, host, port):
    """Start bus traffic monitor"""
    setup_logging(logging_conf)
    logging.info('Starting bus traffic monitor')
    run(host, port)


@main.command()
@click.option('-a', '--algorithm', default='RS256')
@click.option(
    '-f',
    '--key-file',
    default=None,
    help='This argument is mutually exclusive with --private-key',
)
@click.option(
    '-p',
    '--private-key',
    default=None,
    help='This argument is mutually exclusive with --key-file',
)
def token(algorithm, private_key, key_file):
    """Issue access token (JWT)"""
    key = private_key
    if key_file:
        with open(key_file) as f:
            key = f.read()
    print(create_token({}, key, algorithm).decode('utf-8'))  # noqa T001


if __name__ == '__main__':
    main()
