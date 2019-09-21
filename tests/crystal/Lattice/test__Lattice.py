import pytest
import numpy as np

from lattice import Lattice

def test__init__default():
    lattice = Lattice()
    assert isinstance(lattice.a0, float)
    assert isinstance(lattice.H, np.ndarray)
    assert isinstance(lattice.a1, np.ndarray)
    assert isinstance(lattice.a2, np.ndarray)
    assert isinstance(lattice.a3, np.ndarray)

    assert lattice.H.shape == (3,3)
    assert lattice.a1.shape == (3,)
    assert lattice.a2.shape == (3,)
    assert lattice.a3.shape == (3,)
    
