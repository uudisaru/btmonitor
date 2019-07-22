# -*- coding: utf-8 -*-

"""Console script for btmonitor."""
from btmonitor.app import run
from btmonitor.config import setup_logging

import click
import logging


@click.group()
def main():
    """Bus traffic monitor commands"""


@main.command()
@click.option('-c', '--cert-name')
@click.option('-h', '--host', default='0.0.0.0')
@click.option('-l', '--logging-conf', default='logging.ini')
@click.option('-p', '--port', default=8000)
def server(cert_name, host, logging_conf, port):
    """Start bus traffic monitor"""
    setup_logging(logging_conf)
    logging.info('Starting bus traffic monitor')
    run(host, port, cert_name)


if __name__ == '__main__':
    main(obj={})
