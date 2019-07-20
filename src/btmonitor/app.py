# -*- coding: utf-8 -*-

"""Main module."""
from btmonitor.auth.decorators import authorized
from btmonitor.poller import poll_positions
from btmonitor.poller.tallinn import parse_schedule
from btmonitor.poller.tracker import Tracker
from btmonitor.pubsub import Hub
from btmonitor.pubsub import Subscription
from sanic import response
from sanic import Sanic
from websockets import ConnectionClosed

import asyncio
import inspect
import logging
import msgpack


logger = logging.getLogger(__name__)

app = Sanic(__name__)
app.static('/', './frontend/index.html')
app.static('/', './frontend')
hub = Hub(True)
USERS = set()


@app.route('/clients')
@authorized(app.config)
async def test(request):
    return response.json({'clients': len(USERS)})


def register(websocket):
    USERS.add(websocket)
    hub.resume()


def unregister(websocket):
    USERS.remove(websocket)
    if len(USERS) == 0:
        hub.suspend()


@app.websocket('/feed')
async def feed(request, ws):
    register(ws)
    try:
        async for message in ws:
            logger.info('message received')
    except ConnectionClosed:
        logger.info('Connection closed')
    finally:
        logger.info('Unregistering')
        unregister(ws)


async def poller(hub):
    tracker = Tracker(parse_schedule, 'TLN')
    await poll_positions(tracker, hub)


async def publisher(hub):
    with Subscription(hub) as queue:
        while True:
            msg = await queue.get()
            encoded = msgpack.packb(msg)
            for client in USERS:
                try:
                    await client.send(encoded)
                except ConnectionClosed:
                    logger.info('Connection closed')
                    unregister(client)


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


def run(host, port):
    app.run(host=host, port=port)
