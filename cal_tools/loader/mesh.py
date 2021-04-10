import os
import re
import struct
from mmap import ACCESS_READ, mmap
from xml.etree import ElementTree as et
from cal_tools.constants import CAL_OBJECT
from cal_tools.loader.base import CalLoader
from cal_tools.loader.utils import fix_case, get_cases, unpack_chunk, unpack_values
from cal_tools.struct.b_vertex import CalBlendVertex
from cal_tools.struct.face import CalFace
from cal_tools.struct.mesh import CalMesh
from cal_tools.struct.morph import CalMorph
from cal_tools.struct.submesh import CalSubmesh
from cal_tools.struct.vertex import CalVertex


class CalMeshLoader(CalLoader):
    def parse_binary_face(self, cmf: mmap) -> CalFace:
        vertex_ids = unpack_chunk(cmf.read(12), 'i')
        return CalFace(vertex_ids)

    def parse_binary_blend_vertex(self, cmf: mmap, id_: int, uv_count: int) -> CalBlendVertex:
        position = unpack_chunk(cmf.read(12), 'f')
        normal = unpack_chunk(cmf.read(12), 'f')
        uv = None
        for _ in range(uv_count):
            uv = unpack_chunk(cmf.read(8), 'f')
        return CalBlendVertex(id_, position, normal, uv)

    def parse_binary_vertex(self, cmf: mmap, uv_count: int) -> CalVertex:
        position = unpack_chunk(cmf.read(12), 'f')
        normal = unpack_chunk(cmf.read(12), 'f')
        color = unpack_chunk(cmf.read(12), 'f')
        cmf.seek(8, os.SEEK_CUR)
        uv = None
        for _ in range(uv_count):
            uv = unpack_chunk(cmf.read(8), 'f')
        influence_count = struct.unpack('i', cmf.read(4))[0]
        influences = []
        for _ in range(influence_count):
            infl_id, infl_weight = struct.unpack('i', cmf.read(4))[0], struct.unpack('f', cmf.read(4))[0]
            influences.append((infl_id, infl_weight))
        return CalVertex(position, normal, uv, color, influences)

    def parse_binary_morph(self, cmf: mmap, vertex_count: int, uv_count: int) -> CalMorph:
        morph_name_length = struct.unpack('i', cmf.read(4))[0]
        morph_name = cmf.read(morph_name_length - 1).decode('utf-8')
        cmf.seek(1, os.SEEK_CUR)
        blend_vertices = []
        next_blend_vertex_id = struct.unpack('i', cmf.read(4))[0]
        while next_blend_vertex_id < vertex_count:
            blend_vertices.append(self.parse_binary_blend_vertex(cmf, next_blend_vertex_id, uv_count))
            next_blend_vertex_id = struct.unpack('i', cmf.read(4))[0]
        return CalMorph(morph_name, blend_vertices)

    def parse_binary_submesh(self, cmf: mmap) -> CalSubmesh:
        material = struct.unpack('i', cmf.read(4))[0]
        vertex_count = struct.unpack('i', cmf.read(4))[0]
        face_count = struct.unpack('i', cmf.read(4))[0]
        cmf.seek(8, os.SEEK_CUR)
        uv_count = struct.unpack("i", cmf.read(4))[0]
        morph_count = struct.unpack("i", cmf.read(4))[0]
        vertices = []
        for _ in range(vertex_count):
            vertices.append(self.parse_binary_vertex(cmf, uv_count))
        morphs = None
        if morph_count > 0:
            morphs = []
            for _ in range(morph_count):
                morphs.append(self.parse_binary_morph(cmf, vertex_count, uv_count))
        faces = []
        for _ in range(face_count):
            faces.append(self.parse_binary_face(cmf))
        return CalSubmesh(material, vertices, faces, morphs)

    def load_binary(self) -> CAL_OBJECT:
        with open(self.filepath, 'rb') as f, mmap(f.fileno(), 0, access=ACCESS_READ) as cmf:
            cmf.seek(8, os.SEEK_CUR)
            submesh_count = struct.unpack('i', cmf.read(4))[0]
            submeshes = []
            for _ in range(submesh_count):
                submeshes.append(self.parse_binary_submesh(cmf))
        return CalMesh(submeshes)

    def parse_ascii_face(self, face: et.Element, v_id: str) -> CalFace:
        vertex_ids = unpack_values(face.attrib[v_id], int)
        return CalFace(vertex_ids)

    def parse_ascii_blend_vertex(self, blend_vertex: et.Element, v_id: str, position: str,
                                 normal: str, tex: str) -> CalBlendVertex:
        vertex_id = int(blend_vertex.attrib[v_id])
        posn = unpack_values(blend_vertex.find(position).text, float)
        if len(posn) > 0:
            norm = unpack_values(blend_vertex.find(normal).text, float)
            uv = unpack_values(blend_vertex.find(tex).text, float)
            return CalBlendVertex(vertex_id, posn, norm, uv)
        pass

    def parse_ascii_vertex(self, vertex: et.Element, pos: str, norm: str, tex: str,
                           col: str, infl: str, id_: str) -> CalVertex:
        position = unpack_values(vertex.find(pos).text, float)
        normal = unpack_values(vertex.find(norm).text, float)
        uv = unpack_values(vertex.find(tex).text, float)
        color = unpack_values(vertex.find(col).text, float)
        influences = []
        for influence in vertex.iter(infl):
            influence_id, influence_weight = influence.attrib[id_], float(influence.text)
            influences.append((influence_id, influence_weight))
        return CalVertex(position, normal, uv, color, influences)

    def parse_ascii_morph(self, morph: et.Element, uppercase: bool, v_id: str, tex: str) -> CalMorph:
        name = morph.attrib[fix_case('name', uppercase)]
        position, normal = get_cases(uppercase, 'position', 'normal')
        blend_vertices = []
        for blend_vertex in morph.iter(fix_case('blendvertex', uppercase)):
            blend_vertex_object = self.parse_ascii_blend_vertex(blend_vertex, v_id, position, normal, tex)
            if blend_vertex_object:
                blend_vertices.append(blend_vertex_object)
        return CalMorph(name, blend_vertices)

    def parse_ascii_submesh(self, submesh: et.Element, uppercase: bool) -> CalSubmesh:
        material = int(submesh.attrib[fix_case('material', uppercase)])
        pos, norm, col, tex, infl, id_, v_id = get_cases(uppercase, 'pos', 'norm', 'color',
                                                         'texcoord', 'influence', 'id', 'vertexid')
        vertices = []
        for vertex in submesh.iter(fix_case('vertex', uppercase)):
            vertices.append(self.parse_ascii_vertex(vertex, pos, norm, tex, col, infl, id_))
        morphs = []
        for morph in submesh.iter(fix_case('morph', uppercase)):
            morphs.append(self.parse_ascii_morph(morph, uppercase, v_id, tex))
        faces = []
        for face in submesh.iter(fix_case('face', uppercase)):
            faces.append(self.parse_ascii_face(face, v_id))
        return CalSubmesh(material, vertices, faces)

    def load_ascii(self) -> CAL_OBJECT:
        with open(self.filepath, 'r') as f:
            data = f.read()
            match = re.search(r"<mesh", data, re.IGNORECASE)
            uppercase = match.group().isupper()
            start = match.start()
            root = et.fromstring(data[start:])
            submeshes = []
            for submesh in root.iter(fix_case('submesh', uppercase)):
                submeshes.append(self.parse_ascii_submesh(submesh, uppercase))
        return CalMesh(submeshes)

# fpath = "C:/Users/JM729/Desktop/Lynx/Gaming/Virtual/iMVu/Testing/Heads/F-Decrypted.xmf"
# cc = CalMeshLoader(fpath)
# cc.load()
