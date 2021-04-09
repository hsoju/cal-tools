import abc
from cal_tools.constants import CAL_EXTENSIONS, CAL_OBJECT


class CalLoader(abc.ABC):
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.mime = None

    def get_type(self) -> str:
        with open(self.filepath, "rb") as f:
            mime = f.read(3).decode('utf-8')
        if mime in CAL_EXTENSIONS:
            self.mime = mime
            return 'BINARY'
        return 'ASCII'

    @abc.abstractmethod
    def load_binary(self) -> CAL_OBJECT:
        pass

    @abc.abstractmethod
    def load_ascii(self) -> CAL_OBJECT:
        pass

    def load(self) -> CAL_OBJECT:
        if self.get_type() == 'BINARY':
            return self.load_binary()
        return self.load_ascii()
