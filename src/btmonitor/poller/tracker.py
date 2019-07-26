from btmonitor.pos_types import PositionUpdate
from btmonitor.pos_types import PositionUpdateList
from btmonitor.pos_types import ScheduleParser
from btmonitor.time_series import StatCollector
from btmonitor.time_series import timestamp
from typing import Dict
from typing import List
from typing import Optional

import dataclasses
import hashlib
import logging


logger = logging.getLogger(__name__)


@dataclasses.dataclass()
class TimestampedPositionUpdate:
    update: PositionUpdate
    ts: int


class Tracker(StatCollector):
    """Tracker tracks the location of vehicles"""

    def __init__(self, parser: ScheduleParser, area: str):
        """Constructor for Tracker"""
        super().__init__()
        self.area = area
        self.hash: Optional[str] = None
        self.parser = parser
        self.tracks: Dict[str, TimestampedPositionUpdate] = {}
        self._update_stats(self._stats, 0)

    def expire(self, expired_before: int) -> List[str]:
        # Expire tracks/positions that were updated before cutoff time
        expired = []
        for track_id, position in self.tracks.items():
            if position.ts < expired_before:
                expired.append(track_id)
        if expired:
            for track_id in expired:
                del self.tracks[track_id]
            self._update_stats(self._stats, len(self.tracks))
        return expired

    def get_tracks(self) -> PositionUpdateList:
        return {
            'type': 'INI',
            'area': self.area,
            'positions': [track.update for track in self.tracks.values()],
        }

    def send_update(self, position: PositionUpdate) -> bool:
        vehicle_id = position.get('id', None)
        if vehicle_id is None:
            return False
        track = self.tracks.get(vehicle_id, None)
        if not track or track.update != position:
            self.tracks[vehicle_id] = TimestampedPositionUpdate(
                position, timestamp()
            )
            return True
        return False

    def update(self, tracks: str) -> Optional[PositionUpdateList]:
        h = hashlib.md5(bytes(tracks, 'utf-8')).hexdigest()
        if h != self.hash:
            self.hash = h
            updates = [
                pos for pos in self.parser(tracks) if self.send_update(pos)
            ]
            if updates:
                self._update_stats(self._stats, len(self.tracks))
                return {'type': 'POS', 'area': self.area, 'positions': updates}
        return None
