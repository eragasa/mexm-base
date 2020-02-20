import pytest
from distutils import dir_util

import os

from mexm.simulation import VaspSimulation
from mexm.io.vasp import Incar
from mexm.io.vasp import Poscar
from mexm.io.vasp import Potcar
from mexm.io.vasp import Kpoints
from mexm.io.vasp import Outcar
from mexm.io.vasp import Oszicar
from mexm.io.vasp import Contcar

parent_path = os.path.dirname(os.path.abspath(__file__))
@pytest.fixture
def resourcedir(tmpdir, request):
    '''
    Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    https://stackoverflow.com/questions/29627341/pytest-where-to-store-expected-data
    '''
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir

def test___init__():
    o = VaspSimulation()
    assert isinstance(o.incar, Incar)
    assert isinstance(o.poscar, Poscar)
    assert isinstance(o.kpoints, Kpoints)
    assert isinstance(o.potcar, Potcar)
    assert isinstance(o.outcar, Outcar)
    assert isinstance(o.oszicar, Oszicar)
    assert isinstance(o.contcar, Contcar)

def test_read(resourcedir, tmpdir):
    o = VaspSimulation()
    o.read(simulation_path=str(resourcedir))

if __name__ == "__main__":
    src_poscar_path = "POSCAR"
    o_poscar = Poscar()
    o_poscar.read(path=src_poscar_path)