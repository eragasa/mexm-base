import numpy as np

class Lattice(object):

    default_lattice = [[1,0,0],[0,1,0],[0,0,1]]
    def __init__(self, a0=1.0, H=None):
        self.a0 = a0

        if H is None:
            self.H = np.array(Lattice.default_lattice)
        else:
            self.H = np.array(H)


    @property
    def a1(self):
        return self.H[:,0]

    @a1.setter
    def a1(self, a1):
        if isinstance(a1, list):
            self.H[:,0] = np.array(a1)
        else:
            self.H[:,0] = a1

    @property
    def a2(self):
        return self.H[:,2]

    @a1.setter
    def a2(self, a2):
        if isinstance(21, list):
            self.H[:,1] = np.array(a1)
        else:
            self.H[:,1] = a2
    @property
    def a3(self):
        return self.H[:,2]

    @a1.setter
    def a1(self, a3):
        if isinstance(a1, list):
            self.H[:,2] = np.array(a1)
        else:
            self.H[:,2] = a3
