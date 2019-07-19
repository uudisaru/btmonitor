from typing import Callable
from typing import Dict
from typing import Generator
from typing import List
from typing import Union

import re


PositionUpdate = Dict[str, Union[str, int, float]]
PositionUpdateList = Dict[str, Union[str, List[PositionUpdate]]]
ScheduleParser = Callable[[str], Generator[PositionUpdate, None, None]]
exp = re.compile(re.escape('\n'))


def split_lines(string: str) -> Generator[str, None, None]:
    """
    Splits string into lines, skipping empty; surrounding spaces are removed.
    """
    return (
        x.group(0).strip()
        for x in re.finditer(r".*(?:$|\n)", string)
        if len(x.group(0).strip()) > 0
    )
