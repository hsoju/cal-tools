import abc
from cal_tools.constants import CAL_OBJECT


class CalExporter:
    def __init__(self):
        pass

    @abc.abstractmethod
    def export(self, filepath: str, *cal_objects: CAL_OBJECT):
        pass
