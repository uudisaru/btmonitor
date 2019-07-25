# -*- coding: utf-8 -*-

"""Main module."""
from btmonitor.auth.decorators import authorized
from btmonitor.poller import poll_positions
from btmonitor.poller.tallinn import parse_schedule
from btmonitor.poller.tracker import Tracker
from btmonitor.pubsub import Hub
from btmonitor.pubsub import Subscription
from btmonitor.user_registry import UserRegistry
from pathlib import Path
from sanic import response, Sanic
from sanic_cors import CORS
from websockets import ConnectionClosed

import asyncio
import inspect
import logging
import msgpack


logger = logging.getLogger(__name__)

app = Sanic(__name__)
CORS(app, automatic_options=True)
hub = Hub(True)
registry = UserRegistry(hub)


@app.websocket('/feed')
async def feed(request, ws):
    registry.add(ws)
    try:
        async for message in ws:
            logger.info('message received')
    except ConnectionClosed:
        logger.info('Connection closed')
    finally:
        logger.info('Unregistering')
        registry.remove(ws)


@app.route('/clients')
@authorized(app.config)
async def clients(request):
    return response.json({'clients': registry.user_count()})


@app.route('/stats')
@authorized(app.config)
async def stats(request):
    return response.json(registry.stats())


async def poller(hub):
    tracker = Tracker(parse_schedule, 'TLN')
    await poll_positions(tracker, hub)


async def publisher(hub):
    with Subscription(hub) as queue:
        while True:
            msg = await queue.get()
            encoded = msgpack.packb(msg)
            for client in registry.users():
                try:
                    await client.send(encoded)
                except ConnectionClosed:
                    logger.info('Connection closed')
                    registry.remove(client)


@app.listener('after_server_start')
async def after_server_start(app, loop):
    app.add_task(poller(hub))
    app.add_task(publisher(hub))


@app.listener('before_server_stop')
async def before_server_stop(app, loop):
    """Clean up tasks which are not stopped automatically"""
    tasks_to_cancel = {'poller', 'publisher'}
    for task in asyncio.all_tasks(loop):
        frames = task.get_stack(limit=1)
        tb = inspect.getframeinfo(frames[0])
        if tb.function in tasks_to_cancel:
            task.cancel()


def init_ssl(host):
    p = Path(f'/etc/letsencrypt/live/{host}')
    cert = p / 'fullchain.pem'
    if cert.exists():
        return {'cert': str(cert), 'key': str(p / 'privkey.pem')}
    return None


def run(host, port, cert_name):
    ssl = init_ssl(cert_name)
    frontend_dir = Path('./frontend')
    if not frontend_dir.exists():
        frontend_dir = Path('../frontend')
    for fi in frontend_dir.iterdir():
        app.static(
            '/' + fi.name if fi.name != 'index.html' else '/',
            fi.resolve().as_posix(),
        )
    app.run(host=host, port=port, ssl=ssl)
