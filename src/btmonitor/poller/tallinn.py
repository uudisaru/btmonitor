from btmonitor.pos_types import PositionUpdate
from btmonitor.pos_types import split_lines
from typing import Generator


API_TALLINN_BUS_POSITIONS = 'https://transport.tallinn.ee/gps.txt'


def decimal_deg(digits: str) -> float:
    s = digits[:2] + '.' + digits[2:]
    return float(s)


def parse_schedule(schedule: str) -> Generator[PositionUpdate, None, None]:
    for line in split_lines(schedule):
        t, line_no, lon, lat, _, tag, vehicle = line.split(',')
        yield {
            'id': int(vehicle),
            'line': line_no,
            'lat': decimal_deg(lat),
            'lon': decimal_deg(lon),
        }


async def fetch(session):
    async with session.get(API_TALLINN_BUS_POSITIONS) as response:  # noqa R503
        return await response.text()
