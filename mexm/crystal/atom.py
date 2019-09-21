import numpy as np

class Atom(object):
    """description of an atom

    This position is a data structure which contains information about an
    individual atom

    Args:
        symbol (str): the standard ISO symbol for an element
        position (list of float): the position of the atom the units
           are dependent upon use.
        magmom (float): the magnetic moment of the atom.

    Attributes:
        symbol (str): the standard ISO symbol for an element
        position (numpy.ndarray): the position of the atom, usually in direct
            coordinates
        magentic_moment (float): the magnetic moment of the atom
    """
    def __init__(self, symbol, position, magmom = 0):

        self.symbol = symbol
        if isinstance(position,list):
            self.position = np.array(position)
        elif isinstance(position,np.ndarray):
            self.position = position.copy()
        else:
            raise TypeError('position must either be a list of numeric values or a numpy array')
        self.magnetic_moment = magmom

    @property
    def magmom(self):
        return self.magnetic_moment

    @magmom.setter
    def magmom(self, magmom):
        self.magnetic_moment = magmom
