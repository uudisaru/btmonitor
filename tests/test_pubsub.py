from btmonitor.pubsub import Hub
from btmonitor.pubsub import Subscription

import pytest


@pytest.mark.asyncio
async def test_pubsub_single():
    hub: Hub[int] = Hub()
    hub.publish(1)
    with Subscription(hub) as queue:
        assert queue.empty()
        hub.publish(2)
        result = await queue.get()
        assert result == 2
        assert queue.empty()
        hub.suspend()
        hub.publish(3)
        assert queue.empty()
        assert hub.is_suspended()
        hub.resume()
        hub.publish(3)
        assert not queue.empty()
        assert not hub.is_suspended()


@pytest.mark.asyncio
async def test_pubsub_multi():
    hub: Hub[int] = Hub()
    hub.publish(1)
    with Subscription(hub) as queue:
        assert queue.empty()
        hub.publish_all([3, 4])
        result = await queue.get()
        assert result == 3
        assert not queue.empty()
        result = await queue.get()
        assert result == 4
        assert queue.empty()
