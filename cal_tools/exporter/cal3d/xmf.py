import xml.dom.minidom as mini
from xml.etree import ElementTree as et
from cal_tools.constants import CAL_OBJECT
from cal_tools.exporter.base import CalExporter
from cal_tools.struct.b_vertex import CalBlendVertex
from cal_tools.struct.face import CalFace
from cal_tools.struct.mesh import CalMesh
from cal_tools.struct.morph import CalMorph
from cal_tools.struct.submesh import CalSubmesh
from cal_tools.struct.vertex import CalVertex
from cal_tools.exporter.utils import sjoin


class XmfExporter(CalExporter):
    def parse_vertex(self, submesh_tag: et.Element, vertex: CalVertex, id_: int) -> et.Element:
        vertex_tag = et.SubElement(submesh_tag, 'vertex')
        vertex_tag.attrib['id'] = str(id_)
        vertex_tag.attrib['numinfluences'] = str(len(vertex.influences))
        position_tag = et.SubElement(vertex_tag, 'pos')
        position_tag.text = sjoin(vertex.position)
        normal_tag = et.SubElement(vertex_tag, 'norm')
        normal_tag.text = sjoin(vertex.normal)
        color_tag = et.SubElement(vertex_tag, 'color')
        color_tag.text = sjoin(vertex.color)
        uv_tag = et.SubElement(vertex_tag, 'texcoord')
        uv_tag.text = sjoin(vertex.uv)
        for influence_id, influence_weight in vertex.influences:
            influence_tag = et.SubElement(vertex_tag, 'influence')
            influence_tag.attrib['id'] = str(influence_id)
            influence_tag.text = str(influence_weight)
        return vertex_tag

    def parse_blend_vertex(self, morph_tag: et.Element, blend_vertex: CalBlendVertex) -> et.Element:
        blend_vertex_tag = et.SubElement(morph_tag, 'blendvertex')
        blend_vertex_tag.attrib['vertexid'] = str(blend_vertex.id_)
        blend_vertex_tag.attrib['posdiff'] = ''
        position_tag = et.SubElement(blend_vertex_tag, 'position')
        position_tag.text = sjoin(blend_vertex.position)
        normal_tag = et.SubElement(blend_vertex_tag, 'normal')
        normal_tag.text = sjoin(blend_vertex.normal)
        uv_tag = et.SubElement(blend_vertex_tag, 'texcoord')
        uv_tag.text = sjoin(blend_vertex.uv)
        return blend_vertex_tag

    def parse_morph(self, submesh_tag: et.Element, morph: CalMorph) -> et.Element:
        morph_tag = et.SubElement(submesh_tag, 'morph')
        morph_tag.attrib['name'] = morph.name
        morph_tag.attrib['numblendverts'] = str(len(morph.blend_vertices))
        morph_tag.attrib['morphid'] = ''
        for blend_vertex in morph.blend_vertices:
            self.parse_blend_vertex(morph_tag, blend_vertex)
        return morph_tag

    def parse_face(self, submesh_tag: et.Element, face: CalFace) -> et.Element:
        face_tag = et.SubElement(submesh_tag, 'face')
        face_tag.attrib['vertexid'] = sjoin(face.vertices)
        return face_tag

    def parse_submesh(self, mesh_tag: et.Element, submesh: CalSubmesh) -> et.Element:
        submesh_tag = et.SubElement(mesh_tag, 'submesh')
        submesh_tag.attrib['material'] = str(submesh.material)
        submesh_tag.attrib['numvertices'] = str(len(submesh.vertices))
        submesh_tag.attrib['numfaces'] = str(len(submesh.faces))
        submesh_tag.attrib['nummorphs'] = str(len(submesh.morphs))
        submesh_tag.attrib['numlodsteps'] = '0'
        submesh_tag.attrib['numsprings'] = '0'
        submesh_tag.attrib['numtexcoords'] = '1'
        for id_, vertex in enumerate(submesh.vertices):
            self.parse_vertex(submesh_tag, vertex, id_)
        for morph in submesh.morphs:
            self.parse_morph(submesh_tag, morph)
        for face in submesh.faces:
            self.parse_face(submesh_tag, face)
        return submesh_tag

    def parse_mesh(self, mesh: CalMesh) -> et.Element:
        mesh_tag = et.Element('mesh')
        mesh_tag.attrib['numsubmesh'] = str(len(mesh.submeshes))
        for submesh in mesh.submeshes:
            self.parse_submesh(mesh_tag, submesh)
        return mesh_tag

    def export(self, filepath: str, *cal_objects: CAL_OBJECT):
        if len(cal_objects) > 0:
            mesh_object = cal_objects[0]
            if isinstance(mesh_object, CalMesh):
                root = self.parse_mesh(mesh_object)
                raw_xml = et.tostring(root).decode('utf8')
                readable_xml = mini.parseString(raw_xml).toprettyxml()
                with open(filepath, "w") as f:
                    f.write('<header magic="XMF" version="919"/>\n')
                    f.write(readable_xml)
