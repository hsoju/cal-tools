from typing import Iterable
from cal_tools.struct.b_vertex import CalBlendVertex


class CalMorph:
    def __init__(self, name: str, blend_vertices: Iterable[CalBlendVertex]):
        self.name = name
        self.blend_vertices = blend_vertices
