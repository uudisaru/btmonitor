# -*- coding: utf-8 -*-

"""Console script for btmonitor."""
from btmonitor.auth.jwt_auth import create_token
from btmonitor.auth.rsa_utils import decrypt_private_key
from btmonitor.auth.rsa_utils import is_encrypted_rsa_key
from functools import wraps

import aiohttp
import asyncio
import click


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.group()
@click.option('-a', '--algorithm', default='RS256')
@click.option(
    '-f',
    '--key-file',
    default=None,
    help='This argument is mutually exclusive with --private-key',
)
@click.option(
    '-k',
    '--private-key',
    default=None,
    help='This argument is mutually exclusive with --key-file',
)
@click.option(
    '-p',
    '--password',
    default=None,
    help='Decryption password of the private key',
)
@click.pass_context
def main(ctx, private_key, key_file, password, algorithm):
    """Token commands"""
    key = private_key
    if key_file:
        with open(key_file) as f:
            key = f.read()
    if not key:
        return
    if is_encrypted_rsa_key(key):
        if not password:
            password = click.prompt(
                'Please enter private key password', type=str, hide_input=True
            )
        key = decrypt_private_key(key, password)
    ctx.ensure_object(dict)
    ctx.obj['TOKEN'] = create_token({}, key, algorithm).decode('utf-8')


@main.command()
@click.pass_context
def token(ctx):
    """Issue access token (JWT)"""
    click.echo(ctx.obj['TOKEN'])


@main.command()
@click.argument('url')
@click.pass_context
@coro
async def request(ctx, url):
    """Make a request"""
    headers = {'Authorization': 'Bearer ' + ctx.obj['TOKEN']}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            click.echo(await response.text())


if __name__ == '__main__':
    main(obj={})
