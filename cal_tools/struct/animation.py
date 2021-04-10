from typing import Collection
from cal_tools.struct.track import CalTrack


class CalAnimation:
    def __init__(self, duration: float, tracks: Collection[CalTrack]):
        self.duration = duration
        self.tracks = tracks
