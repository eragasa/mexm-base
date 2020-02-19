import pytest

import os
import numpy as np
from mexm.io.vasp import Poscar

def test_Poscar____init__():
    Poscar()

def test_Poscar__read():
    poscar_path = 'Cu_fcc.vasp'
    o = Poscar()
    o.read(path=poscar_path)

def test_Poscar__read__hmatrix():
    poscar_path = 'hmatrixtest.vasp'
    o = Poscar()
    o.read(path=poscar_path)

    expected_h_matrix = np.array([
        [1.,2.,3.],
        [4.,5.,6.],
        [7.,8.,9.]
    ]).T
    assert np.array_equal(o.H, expected_h_matrix)

def test_Poscar__read__latticevectors():
    poscar_path = 'hmatrixtest.vasp'
    o = Poscar()
    o.read(path=poscar_path)

    expected_h_matrix = np.array([
        [1.,2.,3.],
        [4.,5.,6.],
        [7.,8.,9.]
    ]).T
    assert np.array_equal(o.a1, expected_h_matrix[:,0])
    assert np.array_equal(o.a2, expected_h_matrix[:,1])
    assert np.array_equal(o.a3, expected_h_matrix[:,2])

def dev_Poscar__read():
    print(80*'-')
    print('dev_Poscar__read')
    print(80*'-')
    poscar_path = 'hmatrixtest.vasp'
    o = Poscar()
    o.read(path=poscar_path)

    # the h-matrix appears to work
    print('H-Matrix:')
    print(o.H)

    # check the vectors are correct    
    print('a1:',o.a1)
    print('a2:',o.a2)
    print('a3:',o.a3)

def test_Poscar__write():
    src_poscar_path = 'Cu_fcc.vasp'
    dst_poscar_path = 'POSCAR'

    o = Poscar()
    o.read(path=src_poscar_path)
    o.write(path=dst_poscar_path)

def dev_Poscar__write():
    src_poscar_path = 'hmatrixtest.vasp'
    dst_poscar_path = 'POSCAR'

    o = Poscar()
    o.read(path=src_poscar_path)
    o.write(path=dst_poscar_path)

if __name__ == "__main__":
    dev_Poscar__read()
    dev_Poscar__write()
