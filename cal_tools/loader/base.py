import abc
from cal_tools.constants import CAL_EXTENSIONS, CAL_OBJECT


class CalLoader(abc.ABC):
    def __init__(self):
        pass

    @staticmethod
    def get_type(filepath: str) -> str:
        with open(filepath, "rb") as f:
            mime = f.read(3).decode('utf-8')
        if mime in CAL_EXTENSIONS:
            return 'BINARY'
        return 'ASCII'

    @abc.abstractmethod
    def load_binary(self, filepath: str) -> CAL_OBJECT:
        pass

    @abc.abstractmethod
    def load_ascii(self, filepath: str) -> CAL_OBJECT:
        pass

    def load(self, filepath: str) -> CAL_OBJECT:
        if self.get_type(filepath) == 'BINARY':
            return self.load_binary(filepath)
        return self.load_ascii(filepath)
