from btmonitor.poller.tallinn import fetch

import aiohttp
import asyncio
import logging


logger = logging.getLogger(__name__)


async def poll_bus_positions(session, tracker, hub):
    schedule = await fetch(session)
    position_list = tracker.update(schedule)
    logger.info('schedule retrieved')
    if position_list:
        hub.publish(position_list)


async def poll_positions(tracker, hub, interval=5):
    async with aiohttp.ClientSession() as session:
        while True:
            if not hub.is_suspended():
                await poll_bus_positions(session, tracker, hub)
            await asyncio.sleep(interval)
