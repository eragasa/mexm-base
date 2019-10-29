import numpy as np

class BaseSetflFile():
    def __init__(self, path=None):
        assert any([isinstance(path, str), path is None])

        if path is not None:
            self.path = path

        self.comments = []
        self.symbols = []

        self.Nrho = None
        self.drho = None
        self.maxrho = None
        self.rho = []

        self.Nr = None
        self.dr = None
        self.rmax = None
        self.r = {}

        self.pair = {}
        self.embedding = {}
        self.density = {}

    @staticmethod
    def get_interatomic_distance_vector(rmax, Nr):
        assert isinstance(rmax, float)
        assert isinstance(Nr, float)
        assert Nr % 5 == 0

        r = rmax * np.linspace(1, Nr, Nr)/Nr
        dr = rmax / Nr

        return r, dr

    @staticmethod
    def get_electron_density_vector(rho_max, Nrho):
        assert isinstance(rho_max, float)
        assert isintance(Nr, float)
        assert Nr % 5 == 0

        rho = rho_max * np.linspace(1, Nrho, Nrho)/Nrho
        drho = rho_max/ Nrho
        return rho, drho
