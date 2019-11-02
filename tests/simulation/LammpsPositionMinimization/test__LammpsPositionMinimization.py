import pytest
import os, shutil
from collections import OrderedDict
from mexm.structure import SimulationCell
from mexm.simulation import LammpsPositionMinimization, LammpsSimulation
from mexm.potential import BuckinghamPotential

init_kwargs = {
    'name':'test_name',
    'simulation_path':'simulation_path',
    'structure_path':os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'resources','POSCAR'),
    'bulk_structure_name':'MgO_unit_cell'
}
potential_config = OrderedDict([
    ('potential_name','buckingham'),
    ('symbols',['Mg', 'O'])
])

expected_values = {
    'potential':{
        'potential_name':potential_config['potential_name'],
        'potential_type':BuckinghamPotential
    }

}

def cleanup():
    shutil.rmtree(init_kwargs['simulation_path'])

def test__LammpsPositionMinimization__inheritance():
    o = LammpsPositionMinimization(**init_kwargs)
    from mexm.simulation import LammpsSimulation
    assert isinstance(o, LammpsSimulation)

    from mexm.simulation import PositionMinimization
    assert isinstance(o, PositionMinimization)

def test__LammpsPositionMinimization__properties():
    assert LammpsPositionMinimization.simulation_type == 'lammps_min_pos'
    assert LammpsPositionMinimization.is_base_class == False

def test__LammpsPositionMinimization____init__():
    o = LammpsPositionMinimization(**init_kwargs)
    assert not o.is_fullauto
    assert o.potential is None
    assert o.lammps_script is None

    assert o.structure_path == init_kwargs['structure_path']
    assert isinstance(o.structure, SimulationCell)
    assert o.bulk_structure_name == init_kwargs['bulk_structure_name']

    assert o.lammps_input_path == 'lammps.in'
    assert o.lammps_output_path == 'lammps.out'
    assert o.lammps_structure_path == 'lammps.structure'
    assert o.lammps_potentialmod_path == 'potential.mod'
    assert o.lammps_setfl_path is None

    assert o.use_mpi == False
    try:
        lammps_bin = os.environ['LAMMPS_SERIAL_BIN']
        assert o.lammps_bin == os.environ['LAMMPS_SERIAL_BIN']
    except KeyError:
        assert o.lammps_bin is None

    assert os.path.isdir(init_kwargs['simulation_path'])
    cleanup()

def test__configure_potential__w_dict():
    o = LammpsPositionMinimization(**init_kwargs)
    o.configure_potential(potential=potential_config)
    assert isinstance(o.potential,
                      expected_values['potential']['potential_type'])
    cleanup()

def test__lammps_input_file_to_string():
    from mexm.manager import PotentialManager
    o = LammpsPositionMinimization(**init_kwargs)
    o.configure_potential(potential=potential_config)
    assert isinstance(o.lammps_input_file_to_string(), str)
    cleanup()

def dev__lammps_input_file_to_string():
    o = LammpsPositionMinimization(**init_kwargs)
    o.configure_potential(potential=potential_config)
    print(o.lammps_input_file_to_string())
    cleanup()

def dev__set_potential_parameters():
    o = LammpsPositionMinimization(**init_kwargs)
    o.configure_potential(potential=potential_config)
    o.set_potential_parameters()

if __name__ == "__main__":
    dev__lammps_input_file_to_string()
