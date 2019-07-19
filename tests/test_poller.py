from btmonitor.poller import fetch
from btmonitor.poller import poll_bus_positions
from btmonitor.poller.tallinn import parse_schedule
from btmonitor.poller.tracker import Tracker
from btmonitor.pubsub import Hub
from btmonitor.pubsub import Subscription
from tests import make_session

import pytest


@pytest.mark.asyncio
async def test_fetch():
    session = make_session('test')
    assert 'test' == await fetch(session)


@pytest.mark.asyncio
async def test_poll_positions():
    session = make_session(
        """2,17,24715550,59411480,,24,1035
2,17,24687130,59399520,,255,1038"""
    )
    hub = Hub()
    tracker = Tracker(parse_schedule, 'TLN')
    with Subscription(hub) as queue:
        await poll_bus_positions(session, tracker, hub)
        pos = await queue.get()
        positions = pos['positions']
        assert len(positions) == 2
        assert positions[0]['id'] == 1035
        assert positions[1]['id'] == 1038
        assert queue.empty()

        # Repeat is ignored
        await poll_bus_positions(session, tracker, hub)
        assert queue.empty()
