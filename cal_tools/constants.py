from typing import Union
from cal_tools.struct.animation import CalAnimation
from cal_tools.struct.mesh import CalMesh

# Cal3D file formats
CAL_EXTENSIONS = {'CAF', 'CMF', 'CPF', 'CRF', 'CSF'}

# Cal3D objects
CAL_OBJECT = Union[CalAnimation, CalMesh]
