import pytest

import os
from mexm.io.vasp import Poscar

def test_Poscar____init__():
    Poscar()

def test_Poscar__read():
    poscar_path = 'Cu_fcc.vasp'
    o = Poscar()
    o.read(path=poscar_path)

def test_Poscar__write():
    src_poscar_path = 'Cu_fcc.vasp'
    dst_poscar_path = 'POSCAR'

    o = Poscar()
    o.read(path=src_poscar_path)
    o.write(path=dst_poscar_path)


def dev_Poscar__read():
    poscar_path = 'Cu_fcc.vasp'
    o = Poscar()
    o.read(path=poscar_path)

def dev_Poscar__write():
    src_poscar_path = 'hmatrixtest.vasp'
    dst_poscar_path = 'POSCAR'

    o = Poscar()
    o.read(path=src_poscar_path)
    o.write(path=dst_poscar_path)

if __name__ == "__main__":
    dev_Poscar__read()
    dev_Poscar__write()
