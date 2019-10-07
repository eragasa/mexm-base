import numpy as np
import ase.lattice.cubic

from mexm.crystal import SimulationCell
from mexm.elements import ELEMENTS

class FaceCenteredCubic(SimulationCell):

    def __init__(self,symbols):
        SimulationCell.__init__(symbols=symbols)


def get_lattice(a,b=None,c=None,alpha=90.,beta=90.,gamma=90.):
    if b is None and c is None:
        b = a
        c = a
    elif b is None and isinstance(c, float):
        b = a
    else:
        raise ValueError



"""
We start by defining a slab
"""

    
lattice_directions = [[1,-1,0],
                      [1,1,-2],
                      [1,1,1]]

try:
    ase_atoms = ase.lattice.cubic.FaceCenteredCubic(directions=lattice_directions,
                                  size=(1,1,1),
                                  symbol='Fe',
                                  pbc=[0,0,1])
except ValueError as e:
    assert str(e) == 'Cannot guess the fcc lattice constant of an element with crystal structure bcc.'
    print(ELEMENTS['Fe'].covrad)
    print(ELEMENTS['Fe'].atmrad)

def get_lattice_directions(miller):
    pass

miller_surface = [1,1,1]
