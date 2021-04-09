from typing import Iterable
from cal_tools.struct.face import CalFace
from cal_tools.struct.morph import CalMorph
from cal_tools.struct.vertex import CalVertex


class CalSubmesh:
    def __init__(self, material: int, vertices: Iterable[CalVertex], faces: Iterable[CalFace],
                 morphs: Iterable[CalMorph] = None):
        self.material = material
        self.vertices = vertices
        self.faces = faces
        self.morphs = morphs
