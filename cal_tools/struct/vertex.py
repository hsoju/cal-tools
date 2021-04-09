from typing import Collection, Iterable, Tuple


class CalVertex:
    def __init__(self, position: Iterable[float], normal: Iterable[float], uv: Iterable[float],
                 color: Iterable[float] = None, influences: Collection[Tuple[int, float]] = None):
        self.position = position
        self.normal = normal
        self.uv = uv
        self.color = color
        self.influences = influences
