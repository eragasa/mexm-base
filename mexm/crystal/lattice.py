import numpy as np

class Lattice(object):
    """ a crystal lattice

    Args:
        a0 (float): the length of the a1 lattice vector
        H (list of list): a 3x3 matrix containing the lattice vectors as ranks
    """

    default_lattice = [[1,0,0],[0,1,0],[0,0,1]]
    def __init__(self, a0=1.0, H=None):
        self.a0 = a0

        if H is None:
            self.H = np.array(Lattice.default_lattice)
        else:
            self.H = np.array(H)

    @property
    def h1(self):
        return self.H[:,0]

    @h1.setter
    def h1(self, a1):
        if isinstance(h1, list):
            self.H[:,0] = np.array(a1)
        else:
            self.H[:,0] = h1

    @property
    def h2(self):
        return self.H[:,2]

    @h2.setter
    def h2(self, h2):
        if isinstance(21, list):
            self.H[:,1] = np.array(a1)
        else:
            self.H[:,1] = h2
    @property
    def h3(self):
        return self.H[:,2]

    @h3.setter
    def h3(self, h3):
        if isinstance(a1, list):
            self.H[:,2] = np.array(a1)
        else:
            self.H[:,2] = h3

    @property
    def a1(self):
        return self.a0 * self.h1

    @property
    def a2(self):
        return self.a0 * self.h2

    @property
    def a3(self):
        return self.a0 * self.h3

    @property
    def a1_length(self):
        """float: length of the a1 lattice vector"""
        a0 = self.a0
        h1 = self.H[:,0]
        a1_length = a0 * np.dot(h1,h1)**2
        return a1_length

    @property
    def a2_length(self):
        """float: length of the a1 lattice vector"""
        a0 = self.a0
        h2 = self.H[:,1]
        a2_length = a0 * np.dot(h2,h2)**2
        return a2_length

    @property
    def a3_length(self):
        """float: length of the a1 lattice vector"""
        a0 = self.a0
        h3 = self.H[:,2]
        a3_length = a0 * np.dot(h3,h3)**2
        return a3_length

    @property
    def b1(self):
        """numpy.array: this is a 3x1 numpy array, in reciprocal space"""
        a1 = a0 * self.h1
        a2 = a0 * self.h2
        a3 = a0 * self.h3

        b1 = 2 * np.pi * np.cross(a2,a3) / np.dot(a1, np.cross(a2,a3))
        return b1

    @property
    def b2(self):
        """numpy.array: this is a 3x1 numpy array, in reciprocal space"""
        a1 = a0 * self.h1
        a2 = a0 * self.h2
        a3 = a0 * self.h3

        b2 = 2 * np.pi * np.cross(a3,a1) / np.dot(a2, np.cross(a3,a1))
        return b2

    @property
    def b3(self):
        """numpy.array: this is a 3x1 numpy array, in reciprocal space"""
        a1 = a0 * self.h1
        a2 = a0 * self.h2
        a3 = a0 * self.h3

        b3 = 2 * np.pi * np.cross(a1,a2) / np.dot(a3, np.cross(a1,a2))
        return b3
