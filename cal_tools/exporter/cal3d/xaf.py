import xml.dom.minidom as mini
from xml.etree import ElementTree as et
from cal_tools.constants import CAL_OBJECT
from cal_tools.exporter.base import CalExporter
from cal_tools.exporter.utils import sjoin
from cal_tools.struct.animation import CalAnimation
from cal_tools.struct.keyframe import CalKeyframe
from cal_tools.struct.track import CalTrack


class XafExporter(CalExporter):
    def __init__(self):
        super().__init__('.xaf')

    def parse_keyframe(self, track_tag: et.Element, keyframe: CalKeyframe) -> et.Element:
        keyframe_tag = et.SubElement(track_tag, 'keyframe')
        keyframe_tag.attrib['time'] = str(keyframe.time)
        if len(keyframe.translation) > 0:
            translation_tag = et.SubElement(keyframe_tag, 'translation')
            translation_tag.text = sjoin(keyframe.translation)
        rotation_tag = et.SubElement(keyframe_tag, 'rotation')
        rotation_tag.text = sjoin(keyframe.rotation)
        return keyframe_tag

    def parse_track(self, animation_tag: et.Element, track: CalTrack) -> et.Element:
        track_tag = et.SubElement(animation_tag, 'track')
        track_tag.attrib['boneid'] = str(track.bone_id)
        track_tag.attrib['numkeyframes'] = str(len(track.keyframes))
        for keyframe in track.keyframes:
            self.parse_keyframe(track_tag, keyframe)
        return track_tag

    def parse_animation(self, animation: CalAnimation) -> et.Element:
        animation_tag = et.Element('animation')
        animation_tag.attrib['numtracks'] = str(len(animation.tracks))
        animation_tag.attrib['duration'] = str(animation.duration)
        for track in animation.tracks:
            self.parse_track(animation_tag, track)
        return animation_tag

    def export(self, filepath: str, *cal_objects: CAL_OBJECT):
        if len(cal_objects) > 0:
            animation_object = cal_objects[0]
            if isinstance(animation_object, CalAnimation):
                root = self.parse_animation(animation_object)
                raw_xml = et.tostring(root).decode('utf8')
                readable_xml = mini.parseString(raw_xml).toprettyxml()
                with open(filepath, "w") as f:
                    f.write('<header magic="XAF" version="919"/>\n')
                    f.write(readable_xml)
