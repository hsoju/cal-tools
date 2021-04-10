from typing import Collection
from cal_tools.struct.face import CalFace
from cal_tools.struct.morph import CalMorph
from cal_tools.struct.vertex import CalVertex


class CalSubmesh:
    def __init__(self, material: int, vertices: Collection[CalVertex], faces: Collection[CalFace],
                 morphs: Collection[CalMorph] = None):
        self.material = material
        self.vertices = vertices
        self.faces = faces
        self.morphs = morphs if morphs else ()
