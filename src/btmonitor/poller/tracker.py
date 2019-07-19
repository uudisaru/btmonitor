from btmonitor.pos_types import PositionUpdate
from btmonitor.pos_types import PositionUpdateList
from btmonitor.pos_types import ScheduleParser
from typing import Dict
from typing import Optional

import hashlib
import logging


logger = logging.getLogger(__name__)


class Tracker:
    """Tracker tracks the location of vehicles"""

    def __init__(self, parser: ScheduleParser, area: str):
        """Constructor for Tracker"""
        self.area = area
        self.hash: Optional[str] = None
        self.parser = parser
        self.tracks: Dict[str, PositionUpdate] = {}

    def send_update(self, position):
        vehicle_id = position.get('id', None)
        if vehicle_id is None:
            return False
        if self.tracks.get(vehicle_id, None) != position:
            self.tracks[vehicle_id] = position
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
                return {'type': 'POS', 'area': self.area, 'positions': updates}
        return None
