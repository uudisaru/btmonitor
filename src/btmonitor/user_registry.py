from typing import List, Set

from btmonitor.pubsub import Hub
from collections import deque
from datetime import datetime

import dataclasses


@dataclasses.dataclass()
class UsageStat:
    count: int
    ts: int


class UserRegistry:
    """Registry that holds currently connected users (websockets)"""

    def __init__(self, hub: Hub, max_len=1000):
        """Constructor for UserRegistry"""
        self._hub = hub
        self._users = set()
        self._stats = deque(maxlen=max_len)
        self._update_stats(self._stats)

    def _update_stats(self, stats):
        epoch_time = round(datetime.now().timestamp() * 1000)
        count = len(self._users)
        stats.append(UsageStat(count, epoch_time))
        return count

    def add(self, websocket):
        self._users.add(websocket)
        self._hub.resume()
        self._update_stats(self._stats)

    def remove(self, websocket) -> None:
        self._users.remove(websocket)
        if self._update_stats(self._stats) == 0:
            self._hub.suspend()

    def stats(self) -> List[UsageStat]:
        copy = self._stats.copy()
        self._update_stats(copy)
        return copy

    def user_count(self) -> int:
        return len(self._users)

    def users(self) -> Set:
        return self._users
