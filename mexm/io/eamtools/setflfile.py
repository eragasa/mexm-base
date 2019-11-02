from mexm.io.eamtools import SetflReader, SetflWriter
from mexm.potential import get_symbol_pairs
class SetflFile():
    """ class for the setfl

    """
    def __init__(self):
        self.src_file = SetflReader()
        self.dst_file = SetflWriter()

    @property
    def src_path(self):
        return self.src_file.path

    @src_path.setter
    def src_path(self, path):
        assert isinstance(path, str)

        self.src_file.path = path

    @property
    def dst_path(self):
        return self.dst_file.path

    def read(self, path=None):
        if path is not None:
            assert isinstance(path, str)
            self.src_path = path
        self.src_file.read(path=self.src_path)

    def write(self, path=None):
        if path is not None:
            assert isinstance(path, None)
            self.dst_path = path
        self.dst_path.write(path=self.dst_path)
