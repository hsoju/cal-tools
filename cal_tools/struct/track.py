from typing import Collection

from cal_tools.struct.keyframe import CalKeyframe


class CalTrack:
    def __init__(self, bone_id: int, keyframes: Collection[CalKeyframe]):
        self.bone_id = bone_id
        self.keyframes = keyframes
