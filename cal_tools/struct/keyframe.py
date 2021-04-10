from typing import Iterable


class CalKeyframe:
    def __init__(self, time: float, rotation: Iterable[float], translation: Iterable[float] = None):
        self.time = time
        self.rotation = rotation
        self.translation = translation if translation else ()
