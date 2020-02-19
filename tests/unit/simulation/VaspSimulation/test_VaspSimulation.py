import pytest

from mexm.simulation import VaspSimulation
from mexm.io.vasp import Incar
from mexm.io.vasp import Poscar
from mexm.io.vasp import Potcar
from mexm.io.vasp import Kpoints
from mexm.io.vasp import Outcar
from mexm.io.vasp import Oszicar
from mexm.io.vasp import Contcar

def test____init__():
    o = VaspSimulation()
    assert isinstance(o.incar, Incar)
    assert isinstance(o.poscar, Poscar)
    assert isinstance(o.kpoints, Kpoints)
    assert isinstance(o.potcar, Potcar)
    assert isinstance(o.outcar, Outcar)
    assert isinstance(o.oszicar, Oszicar)
    assert isinstance(o.contcar, Contcar)

def test__read():
    o = VaspSimulation()
    o.read(simulation_path="./")