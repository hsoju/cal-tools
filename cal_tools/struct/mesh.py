from typing import Collection
from cal_tools.struct.submesh import CalSubmesh


class CalMesh:
    def __init__(self, submeshes: Collection[CalSubmesh]):
        self.submeshes = submeshes
