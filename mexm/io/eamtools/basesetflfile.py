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
        self.r_max = None
        self.r = {}

        self.pair = {}
        self.embedding = {}
        self.density = {}

    @staticmethod
    def get_interatomic_distance_vector(r_max, N_r):
        assert isinstance(r_max, float)
        assert isinstance(N_r, float)
        assert N_r % 5 == 0

        r = r_max * np.linspace(1, N_r, N_r)/N_r
        dr = r_max / N_r

        return r, dr

    @staticmethod
    def get_electron_density_vector(rho_max, N_rho):
        assert isinstance(rho_max, float)
        assert isintance(N_r, float)
        assert N_r % 5 == 0

        rho = rho_max * np.linspace(1, N_rho, N_rho)/N_rho
        drho = rho_max/ N_rho
        return rho, drho
