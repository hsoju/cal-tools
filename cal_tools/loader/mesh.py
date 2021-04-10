import os
import struct
from mmap import ACCESS_READ, mmap
from cal_tools.constants import CAL_OBJECT
from cal_tools.loader.base import CalLoader
from cal_tools.loader.utils import unpack_chunk
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

    def parse_morph(self, cmf: mmap, vertex_count: int, uv_count: int) -> CalMorph:
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
                morphs.append(self.parse_morph(cmf, vertex_count, uv_count))
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

    def load_ascii(self) -> CAL_OBJECT:
        pass
