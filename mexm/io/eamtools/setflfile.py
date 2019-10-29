from mexm.io.eamtools import SetflReader, SetflWriter

class EamSetflFile():
    """ class for the setfl

    """
    def __init__(self):
        self.src_file = SetflReader()
        self.dst_file = SetflWriter()

    @property
    def src_path(self):
        return self.src_file.path

    @property
    def dst_path(self):
        return self.dst_file.path

    def read(self, path=None):
        if path is not None:
            assert isinstance(path, None)
            self.src_path = path
        self.src_path.read(path=self.src_path)

    def write(self, path=None):
        if path is not None:
            assert isinstance(path, None)
            self.dst_path = path
        self.dst_path.write(path=self.dst_path)s
