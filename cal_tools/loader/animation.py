import os
import re
import struct
from mmap import ACCESS_READ, mmap
from xml.etree import ElementTree as et
from cal_tools.constants import CAL_OBJECT
from cal_tools.loader.base import CalLoader
from cal_tools.loader.utils import unpack_chunk, unpack_values
from cal_tools.struct.animation import CalAnimation
from cal_tools.struct.keyframe import CalKeyframe
from cal_tools.struct.track import CalTrack


class CalAnimationLoader(CalLoader):
    def load_binary_keyframe(self, caf: mmap) -> CalKeyframe:
        time = struct.unpack('f', caf.read(4))[0]
        translation = unpack_chunk(caf.read(12), 'f')
        translation = None if sum(translation) > 1000000000 else translation
        rotation = unpack_chunk(caf.read(16), 'f')
        return CalKeyframe(time, rotation, translation)

    def load_binary_track(self, caf: mmap) -> CalTrack:
        bone_id = struct.unpack('i', caf.read(4))[0]
        keyframe_count = struct.unpack('i', caf.read(4))[0]
        keyframes = [self.load_binary_keyframe(caf) for _ in range(keyframe_count)]
        return CalTrack(bone_id, keyframes)

    def load_binary(self) -> CAL_OBJECT:
        with open(self.filepath, 'rb') as f, mmap(f.fileno(), 0, access=ACCESS_READ) as caf:
            caf.seek(12, os.SEEK_CUR)
            duration = struct.unpack('f', caf.read(4))[0]
            track_count = struct.unpack('i', caf.read(4))[0]
            tracks = [self.load_binary_track(caf) for _ in range(track_count)]
        return CalAnimation(duration, tracks)

    def load_ascii_keyframe(self, keyframe: et.Element) -> CalKeyframe:
        time = float(keyframe.attrib['time'])
        rotation = unpack_values(keyframe.find('rotation').text, float)
        translation_tag = keyframe.find('translation')
        translation = None
        if translation_tag is not None:
            translation = unpack_values(translation_tag.text, float)
        return CalKeyframe(time, rotation, translation)

    def load_ascii_track(self, track: et.Element) -> CalTrack:
        bone_id = int(track.attrib['boneid'])
        keyframes = [self.load_ascii_keyframe(keyframe) for keyframe in track.iter('keyframe')]
        return CalTrack(bone_id, keyframes)

    def load_ascii(self) -> CAL_OBJECT:
        with open(self.filepath, 'r') as f:
            data = f.read()
            match = re.search(r"<animation", data, re.IGNORECASE)
            data = data.lower()
            root = et.fromstring(data[match.start():])
            duration = float(root.attrib['duration'])
            tracks = [self.load_ascii_track(track) for track in root.iter('track')]
        return CalAnimation(duration, tracks)
