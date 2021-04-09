from typing import Iterable, Tuple
from cal_tools.struct.vertex import CalVertex


class CalBlendVertex(CalVertex):
    def __init__(self, id_: int, position: Iterable[float], normal: Iterable[float], uv: Iterable[float]):
        super().__init__(position, normal, uv)
