from collections import deque
from datetime import datetime
from itertools import islice
from typing import Deque
from typing import Generic
from typing import List
from typing import MutableSequence
from typing import TypeVar

import dataclasses


T = TypeVar('T')


@dataclasses.dataclass()
class TimeSeriesEntry(Generic[T]):
    data: T
    ts: int


CountEntry = TimeSeriesEntry[int]


def timestamp() -> int:
    """Get current timestamp as Unix epoch time in milliseconds"""
    return round(datetime.now().timestamp() * 1000)


class StatCollector:
    def __init__(self, max_len=1000):
        """Collector of time series data"""
        self._stats: Deque[CountEntry] = deque(maxlen=max_len)
        self._update_stats(self._stats, 0, True)

    def stats(self) -> List[TimeSeriesEntry]:
        copy = list(islice(self._stats, None))
        last = copy[-1]
        self._update_stats(copy, last.data, True)
        return copy

    @staticmethod
    def _update_stats(
        stats: MutableSequence[CountEntry],
        count: int,
        needs_update: bool = False,
    ) -> None:
        """Add new time series entry if it differs from last entry"""
        num_stats = len(stats)
        if not needs_update:
            needs_update = num_stats == 0 or (
                num_stats > 0 and stats[-1].data != count
            )
        if needs_update:
            stats.append(TimeSeriesEntry(count, timestamp()))
        return count
