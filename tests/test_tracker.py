from btmonitor.poller.tallinn import parse_schedule
from btmonitor.poller.tracker import Tracker
from btmonitor.pos_types import PositionUpdate
from btmonitor.time_series import timestamp
from typing import List


LOCATIONS = """2,17,24715550,59411480,,24,1035
2,17,24687130,59399520,,255,1038
2,24A,24656700,59406400,,12,1047
2,36,24729690,59403060,,211,1067
2,40,24713100,59441220,,307,1070
"""


def test_send_update():
    tracker = Tracker(parse_schedule, '')
    pos = {'id': 97, 'lon': 59.01, 'lat': 24.41}
    assert tracker.send_update(pos)
    assert tracker.send_update(pos) is False


def test_send_update_no_id():
    tracker = Tracker(parse_schedule, '')
    pos = {'lon': 59.01, 'lat': 24.41}
    assert tracker.send_update(pos) is False


def test_update():
    tracker = Tracker(parse_schedule, '')
    update = tracker.update(LOCATIONS)
    assert update is not None
    assert isinstance(update['positions'], list)
    positions: List[PositionUpdate] = update['positions']
    assert len(positions) == 5

    assert tracker.update(LOCATIONS) is None

    new_locations = LOCATIONS.replace('24713100,59441220', '24715100,59441220')
    update = tracker.update(new_locations)
    assert update is not None
    assert isinstance(update['positions'], list)
    positions = update['positions']
    assert update is not None
    assert len(positions) == 1
    assert positions[0]['line'] == '40'


def test_update_no_id():
    def no_ids(_):
        yield {'lon': 59.01, 'lat': 24.41}

    tracker = Tracker(no_ids, '')
    assert tracker.update(LOCATIONS) is None


def test_expiry():
    tracker = Tracker(parse_schedule, '')
    update = tracker.update(LOCATIONS)
    now = timestamp()
    assert 0 == len(tracker.expire(now - 60 * 1000))
    assert len(update['positions']) == len(tracker.expire(now + 60 * 1000))
    assert len(tracker.tracks) == 0


def test_get_tracks():
    tracker = Tracker(parse_schedule, '')
    update = tracker.update(LOCATIONS)
    tracks = tracker.get_tracks()
    assert update['positions'] == tracks['positions']
