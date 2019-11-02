import pytest
import os, shutil
from collections import OrderedDict
from mexm.structure import SimulationCell
from mexm.simulation import LammpsSimulation

kwargs = {
    'name':'test_name',
    'simulation_path':'simulation_path',
    'structure_path':os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'resources','POSCAR'),
    'bulk_structure_name':None
}
potential_config = OrderedDict([
    ('potential_name','buckingham'),
    ('symbols',['Mg', 'O'])
])
expected_values = {}
from mexm.potential import BuckinghamPotential
expected_values['buckingham'] = {
    'potential':BuckinghamPotential
}

def test____init__():
    simulation = LammpsSimulation(**kwargs)
    assert not simulation.is_fullauto
    assert simulation.potential is None
    assert simulation.lammps_script is None

    assert simulation.structure_path == kwargs['structure_path']
    assert isinstance(simulation.structure, SimulationCell)
    assert simulation.bulk_structure_name == kwargs['bulk_structure_name']

    assert simulation.lammps_input_path == 'lammps.in'
    assert simulation.lammps_output_path == 'lammps.out'
    assert simulation.lammps_structure_path == 'lammps.structure'
    assert simulation.lammps_potentialmod_path == 'potential.mod'
    assert simulation.lammps_setfl_path is None

    assert simulation.use_mpi == False
    try:
        lammps_bin = os.environ['LAMMPS_SERIAL_BIN']
        assert simulation.lammps_bin == os.environ['LAMMPS_SERIAL_BIN']
    except KeyError:
        assert simulation.lammps_bin is None

    assert os.path.isdir(kwargs['simulation_path'])
    shutil.rmtree(kwargs['simulation_path'])

def test__configure_potential__w_dict():
    simulation = LammpsSimulation(**kwargs)
    simulation.configure_potential(potential=potential_config)
    assert isinstance(simulation.potential,
                      expected_values['buckingham']['potential'])
    shutil.rmtree(kwargs['simulation_path'])

def test__lammps_input_file_to_string():
    from mexm.manager import PotentialManager
    simulation = LammpsSimulation(**kwargs)
    simulation.configure_potential(potential=potential_config)
    assert isinstance(simulation.lammps_input_file_to_string(), str)
    shutil.rmtree(kwargs['simulation_path'])

def dev__lammps_input_file_to_string():
    simulation = LammpsSimulation(**kwargs)
    simulation.configure_potential(potential=potential_config)
    print(simulation.lammps_input_file_to_string())
    shutil.rmtree(kwargs['simulation_path'])

def dev__set_potential_parameters():
    o = LammpsSimulation(**kwargs)
    o.configure_potential(potential=potential_config)
    o.set_potential_parameters()

if __name__ == "__main__":
    dev__lammps_input_file_to_string()
