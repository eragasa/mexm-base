import pytest
from typing import Dict

from mexm.simulation import GulpStructuralMinimization
from mexm.simulation import GulpStaticCalculation
from mexm.simulation import GulpPositionMinimization
from mexm.simulation import GulpPhononCalculation
from mexm.simulation import LammpsStructuralMinimization
from mexm.simulation import LammpsStaticCalculation
from mexm.simulation import LammpsPositionMinimization
from mexm.simulation import LammpsNptSimulation
from mexm.simulation import LammpsNvtSimulation
from mexm.simulation import VaspStructuralMinimization
from mexm.simulation import VaspStaticCalculation
from mexm.simulation import VaspPositionMinimization
from mexm.simulation import VaspPhononCalculation

from mexm.simulation import Simulation
from mexm.simulation import SimulationFactory

@pytest.fixture
def objSimulationFactory() -> SimulationFactory:
    return SimulationFactory

@pytest.fixture
def expected_factories() -> Dict[str, Simulation]:

    expected_factories = {
        'gulp_min_all': GulpStructuralMinimization,
        'gulp_min_none':GulpStaticCalculation,
        'gulp_min_positions': GulpPositionMinimization,
        'gulp_phonons': GulpPhononCalculation,
        'lammps_min_all': LammpsStructuralMinimization,
        'lammps_min_none': LammpsStaticCalculation,
        'lammps_min_pos': LammpsPositionMinimization,
        'lammps_npt': LammpsNptSimulation,
        'lammps_nvt': LammpsNvtSimulation,
        'vasp_min_all': VaspStructuralMinimization,
        'vasp_min_none': VaspStaticCalculation,
        'vasp_min_positions': VaspPositionMinimization,
        'vasp_phonons': VaspPhononCalculation
    }
    return expected_factories

def test_static_factories(expected_factories: Dict[str, Simulation]):  
    assert set(list(SimulationFactory.factories.keys())) \
        == set(list(expected_factories.keys()))

    for k, v in expected_factories.items():
        assert k in SimulationFactory.factories
        assert SimulationFactory.factories[k] == v

def test___init__(expected_factories):
    obj = SimulationFactory()

    assert set(list(obj.factories.keys())) == set(list(expected_factories.keys()))
    for k, v in expected_factories.items():
        assert k in obj.factories
        assert obj.factories[k] == v
