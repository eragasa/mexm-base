import pytest
import numpy as np

from mexm.structure import Lattice

def dev__Lattice():
    lattice = Lattice()
    print(lattice)

def test__init__default():
    lattice = Lattice()
    assert isinstance(lattice.a0, float)
    assert isinstance(lattice.H, np.ndarray)
    assert isinstance(lattice.a1, np.ndarray)
    assert isinstance(lattice.a2, np.ndarray)
    assert isinstance(lattice.a3, np.ndarray)

    assert lattice.H.shape == (3,3)

    assert lattice.h1.shape == (3,)
    assert lattice.h2.shape == (3,)
    assert lattice.h3.shape == (3,)
    assert np.array_equal(lattice.h1, np.array([1,0,0]))
    assert np.array_equal(lattice.h2, np.array([0,1,0]))
    assert np.array_equal(lattice.h3, np.array([0,0,1]))

    assert lattice.a1.shape == (3,)
    assert lattice.a2.shape == (3,)
    assert lattice.a3.shape == (3,)

    a0 = lattice.a0
    assert np.array_equal(lattice.a1, a0*np.array([1,0,0]))
    assert np.array_equal(lattice.a2, a0*np.array([0,1,0]))
    assert np.array_equal(lattice.a3, a0*np.array([0,0,1]))

def test__modify_a0():
    lattice = Lattice()
    lattice.a0 = 2
    a0 = lattice.a0
    assert np.array_equal(lattice.a1, a0*np.array([1,0,0]))
    assert np.array_equal(lattice.a2, a0*np.array([0,1,0]))
    assert np.array_equal(lattice.a3, a0*np.array([0,0,1]))

def test__to_dict():
    lattice = Lattice()
    obj_dict = lattice.to_dict()
    assert isinstance(obj_dict, dict)
    assert obj_dict['a0'] == lattice.a0
    assert np.array_equal(obj_dict['H'], lattice.H)

def test__initialize_from_dict():
    lattice_original = Lattice()
    obj_dict = lattice_original.to_dict()

    lattice_copy = Lattice.initialize_from_dict(obj_dict=obj_dict)
    assert isinstance(lattice_copy, Lattice)
    assert np.array_equal(lattice_original.a0, lattice_copy.a0)
    assert np.array_equal(lattice_original.H, lattice_copy.H)

def test__h1_setter__list():
    h1 = [0.0, 2.10597, 2.10597]
    lattice = Lattice()
    lattice.h1 = h1
    assert np.array_equal(lattice.h1, np.array(h1))

def test__h1_setter____numpy_array():
    h1 = [0.0, 2.10597, 2.10597]
    lattice = Lattice()
    lattice.h1 = np.array(h1)
    assert np.array_equal(lattice.h1, np.array(h1))

def test__h2_setter____list():
    h2 = [0.0, 2.10597, 2.10597]
    lattice = Lattice()
    lattice.h2 = h2
    assert np.array_equal(lattice.h2, np.array(h2))

def test__h2_setter____numpy_array():
    h2 = [0.0, 2.10597, 2.10597]
    lattice = Lattice()
    lattice.h2 = np.array(h2)
    assert np.array_equal(lattice.h2, np.array(h2))

def test__h3_setter____list():
    h3 = [0.0, 2.10597, 2.10597]
    lattice = Lattice()
    lattice.h3 = h3
    assert np.array_equal(lattice.h3, np.array(h3))

def test__h3_setter__numpy_array():
    h3 = [0.0, 2.10597, 2.10597]
    lattice = Lattice()
    lattice.h3 = np.array(h3)
    assert np.array_equal(lattice.h3, np.array(h3))
if __name__ == "__main__":
    dev__Lattice()
