import pytest
from typing import Dict
from mexm.simulation import Simulation
from mexm.simulation import SimulationFactory

@pytest.fixture
def objSimulationFactory() -> SimulationFactory:
    return SimulationFactory

@pytest.fixture
def expected_factories() -> Dict(s, Simulation):

    expected factories = {
        'gulp_min_all': mexm.simulation.GulpStructuralMinimization,
        'gulp_min_none': mexm.simulation.GulpStaticCalculation,
        'gulp_min_positions': mexm.simulation.GulpPositionMinimization,
        'gulp_phonons': mexm.simulation.GulpPhononCalculation,
        'lammps_min_all': mexm.simulation.lmps_min_all.LammpsStructuralMinimization,
        'lammps_min_none': mexm.simulation.lmps_min_none.LammpsStaticCalculation,
        'lammps_min_pos': mexm.simulation.lmps_min_pos.LammpsPositionMinimization,
        'lammps_npt': mexm.simulation.lmps_npt.LammpsNptSimulation,
        'lammps_nvt': mexm.simulation.LammpsNvtSimulation,
        'vasp_min_all': mexm.simulation.VaspStructuralMinimization,
        'vasp_min_none': mexm.simulation.VaspStaticCalculation,
        'vasp_min_positions': mexm.simulation.VaspPositionMinimization,
        'vasp_phonons': mexm.simulation.VaspPhononCalculation
    }
    return expected_factories

def test___init__():
    obj = SimulationFactory(expected_factories)

    assert obj.factories.keys() == expected_factories
    for k, v in expected_factories.items():
