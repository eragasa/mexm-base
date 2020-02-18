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