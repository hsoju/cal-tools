from typing import Iterable
from cal_tools.struct.submesh import CalSubmesh


class CalMesh:
    def __init__(self, submeshes: Iterable[CalSubmesh]):
        self.submeshes = submeshes
