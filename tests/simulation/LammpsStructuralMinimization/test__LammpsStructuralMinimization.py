import pytest
import os, shutil
from collections import OrderedDict
from mexm.structure import SimulationCell
from mexm.potential import BuckinghamPotential
from mexm.simulation import LammpsStructuralMinimization

init_kwargs = {
    'name':'test_simulation_name',
    'simulation_path':'test_simulation_directory',
    'structure_path':os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'resources',
        'POSCAR'),
    'bulk_structure_name':None
}

potential_config = OrderedDict([
    ('potential_name','buckingham'),
    ('symbols',['Mg', 'O'])
])

expected_values = {
    'potential':{
        'potential_name':'buckingham',
        'potential_type':BuckinghamPotential
    }
}


def cleanup():
    shutil.rmtree(init_kwargs['simulation_path'])

def test__LammpsStructuralMinimization__properties():
    assert LammpsStructuralMinimization.simulation_type == 'lammps_min_all'
    assert LammpsStructuralMinimization.is_base_class == False

def dev__LammpsStructuralMinimization____init__():
    o = LammpsStructuralMinimization(**init_kwargs)
    cleanup()

def test__LammpsStructuralMinimization____init__():
    o = LammpsStructuralMinimization(**init_kwargs)

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

    cleanup()

def test__configure_potential__w_dict():
    o = LammpsStructuralMinimization(**init_kwargs)
    o.configure_potential(potential=potential_config)
    assert isinstance(o.potential,
                      expected_values['potential']['potential_type'])
    cleanup()

def test__lammps_input_file_to_string():
    from mexm.manager import PotentialManager
    o = LammpsStructuralMinimization(**init_kwargs)
    o.configure_potential(potential=potential_config)
    assert isinstance(o.lammps_input_file_to_string(), str)
    cleanup()


if __name__ == '__main__':
    o = LammpsStructuralMinimization(**init_kwargs)
