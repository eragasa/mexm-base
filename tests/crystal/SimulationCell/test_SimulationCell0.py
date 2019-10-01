import pytest
import numpy as np
from mexm.crystal import Atom
from mexm.crystal import Lattice

from simulationcell import SimulationCell


def test__init__noargs():
    cell = SimulationCell()
    assert isinstance(cell.lattice, Lattice)

    # testing properties
    assert isinstance(cell.H, np.ndarray)
    np.testing.assert_array_equal(cell.H,
                                  cell.lattice.H)

    assert isinstance(cell.a0, float)
    assert cell.a0 == cell.lattice.a0
    assert cell.atomic_basis == []
    assert cell.vacancies ==  []
    assert cell.interstitials == []

def test__H__set_w_list_of_lists():
    cell = SimulationCell()
    cell.H = [[1,2,3],
              [4,5,6],
              [7,8,9]]

    np.testing.assert_array_equal(cell.h1,
                                  np.array([1,4,7]))
    np.testing.assert_array_equal(cell.h2,
                                  np.array([2,5,8]))
    np.testing.assert_array_equal(cell.h3,
                                  np.array([3,6,9]))

def test__H__set_w_numpyarray():
    cell = SimulationCell()
    cell.H = np.array([[1,2,3],
                       [4,5,6],
                       [7,8,9]])

    np.testing.assert_array_equal(cell.h1,
                                  np.array([1,4,7]))
    np.testing.assert_array_equal(cell.h2,
                                  np.array([2,5,8]))
    np.testing.assert_array_equal(cell.h3,
                                  np.array([3,6,9]))

def test__h1__set_w_list():
    cell = SimulationCell()
    cell.H = [[1,2,3],[4,5,6],[7,8,9]]
    cell.h1 = [1,2,3]

    np.testing.assert_array_equal(cell.h1,
                                  np.array([1,2,3]))
    np.testing.assert_array_equal(cell.h2,
                                  np.array([2,5,8]))
    np.testing.assert_array_equal(cell.h3,
                                  np.array([3,6,9]))

def test__h1__set_w_numpyarray():
    cell = SimulationCell()
    cell.H = [[1,2,3],[4,5,6],[7,8,9]]
    cell.h1 = np.array([1,2,3])

    np.testing.assert_array_equal(cell.h1,
                                  np.array([1,2,3]))
    np.testing.assert_array_equal(cell.h2,
                                  np.array([2,5,8]))
    np.testing.assert_array_equal(cell.h3,
                                  np.array([3,6,9]))

def test__h2__set_w_list():
    cell = SimulationCell()
    cell.H = [[1,2,3],[4,5,6],[7,8,9]]
    cell.h2 = [4,5,6]

    np.testing.assert_array_equal(cell.h1,
                                  np.array([1,4,7]))
    np.testing.assert_array_equal(cell.h2,
                                  np.array([4,5,6]))
    np.testing.assert_array_equal(cell.h3,
                                  np.array([3,6,9]))

def test__h2__set_w_numpyarray():
    cell = SimulationCell()
    cell.H = [[1,2,3],[4,5,6],[7,8,9]]
    cell.h2 = np.array([4,5,6])

    np.testing.assert_array_equal(cell.h1,
                                  np.array([1,4,7]))
    np.testing.assert_array_equal(cell.h2,
                                  np.array([4,5,6]))
    np.testing.assert_array_equal(cell.h3,
                                  np.array([3,6,9]))

def test__h3__set_w_list():
    cell = SimulationCell()
    cell.H = [[1,2,3],[4,5,6],[7,8,9]]
    cell.h3 = [7,8,9]

    np.testing.assert_array_equal(cell.h1, np.array([1,4,7]))
    np.testing.assert_array_equal(cell.h2, np.array([2,5,8]))
    np.testing.assert_array_equal(cell.h3, np.array([7,8,9]))

def test__h3__set_w_numpyarray():
    cell = SimulationCell()
    cell.H = [[1,2,3],[4,5,6],[7,8,9]]
    cell.h3  = np.array([7,8,9])

    np.testing.assert_array_equal(cell.h1,np.array([1,4,7]))
    np.testing.assert_array_equal(cell.h2,np.array([2,5,8]))
    np.testing.assert_array_equal(cell.h3,np.array([7,8,9]))


if __name__ == "__main__":
    cell = SimulationCell()
