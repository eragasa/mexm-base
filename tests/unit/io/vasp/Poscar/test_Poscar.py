import pytest

import os
import numpy as np
from mexm.io.vasp import Poscar

parent_path = os.path.dirname(os.path.abspath(__name__))

def test_Poscar____init__():
    Poscar()

def test_read():
    poscar_path = os.path.join(
        parent_path, 'resources', 'Si_primitive.vasp'
    )

    o = Poscar()
    o.read(path=poscar_path)

def test_read__check_h_matrix():
    poscar_path = os.path.join(parent_path, 'resources', 'hmatrixtest.vasp')

    o = Poscar()
    o.read(path=poscar_path)

    h_matrix = np.array([[1.,2.,3.],[4.,5.,6.], [7.,8.,9.]]).T
    assert np.array_equal(o.H, h_matrix)

def test_read__check_lattice_vectors():
    poscar_path = os.path.join(parent_path, 'resources', 'hmatrixtest.vasp')
    h_matrix = np.array([[1.,2.,3.],[4.,5.,6.],[7.,8.,9.]]).T

    o = Poscar()
    o.read(path=poscar_path)
    assert np.array_equal(o.a1, h_matrix[:,0])
    assert np.array_equal(o.a2, h_matrix[:,1])
    assert np.array_equal(o.a3, h_matrix[:,2])

def dev_read():
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

@pytest.fixture
def src_poscar_path():
    poscar_name = 'Si_primitive.vasp'
    return os.path.join(parent_path, 'resources', poscar_name)

def test_write(src_poscar_path, tmpdir):
    dst_poscar_path = os.path.join(tmpdir, 'POSCAR')

    o = Poscar()
    o.read(path=src_poscar_path)
    o.write(path=dst_poscar_path)

    assert os.path.isfile(dst_poscar_path)

def dev_write():
    src_path = os.path.join(parent_path, 'resources', 'Si_primitive.vasp')
    dst_path = 'POSCAR'

    o = Poscar()
    o.read(path=src_path)
    o.write(path=dst_path)

if __name__ == "__main__":
    dev_read()
    dev_write()
