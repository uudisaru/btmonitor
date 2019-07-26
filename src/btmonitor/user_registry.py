from btmonitor.pubsub import Hub
from btmonitor.time_series import StatCollector
from typing import Set


class UserRegistry(StatCollector):
    """Registry that holds currently connected users (websockets)"""

    def __init__(self, hub: Hub, max_len=1000):
        """Constructor for UserRegistry"""
        super().__init__(max_len)
        self._hub = hub
        self._users = set()
        self._update_stats(self._stats, 0)

    def add(self, websocket):
        self._users.add(websocket)
        self._hub.resume()
        self._update_stats(self._stats, self.user_count())

    def remove(self, websocket) -> None:
        self._users.remove(websocket)
        if self._update_stats(self._stats, self.user_count()) == 0:
            self._hub.suspend()

    def user_count(self) -> int:
        return len(self._users)

    def users(self) -> Set:
        return self._users
