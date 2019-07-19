from typing import Any
from typing import Generic
from typing import Sequence
from typing import Set
from typing import TypeVar

import asyncio


T = TypeVar('T')


class Hub(Generic[T]):
    def __init__(self, suspended=False) -> None:
        self.subscriptions: Set['asyncio.Queue[T]'] = set()
        self.suspended = suspended

    def resume(self):
        self.suspended = False

    def suspend(self):
        self.suspended = True

    def is_suspended(self):
        return self.suspended

    def publish(self, message: T) -> None:
        if not self.suspended:
            for queue in self.subscriptions:
                queue.put_nowait(message)

    def publish_all(self, messages: Sequence[T]) -> None:
        if not self.suspended:
            for message in messages:
                for queue in self.subscriptions:
                    queue.put_nowait(message)


class Subscription(Generic[T]):
    def __init__(self, hub: Hub[T]):
        self.hub = hub
        self.queue: 'asyncio.Queue[T]' = asyncio.Queue()

    def __enter__(self) -> 'asyncio.Queue[T]':
        self.hub.subscriptions.add(self.queue)
        return self.queue

    def __exit__(self, t: Any, value: Any, traceback: Any) -> None:
        self.hub.subscriptions.remove(self.queue)
