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

configuration = {
    'simulation':{
        'name':'MgO_NaCl.lmps_min_pos',
        'simulation_path':'test_simulation_directory'},
    'structures':{
        'structure_name':'MgO_NaCl_unit',
        'structure_path':'MgO_NaCl_unit.vasp',
        'bulk_structure_name':'MgO_NaCl_fr',
        'bulk_structure_path':'MgO_NaCl_fr.vasp'},
    'potential':{
        'potential_name':'buckingham',
        'symbols':['Mg', 'O'],
        'parameters':{
            'cutoff':12.0,
            'Mg_chrg':+2.0,
            'O_chrg':-2.0,
            'MgMg_A':0.0,
            'MgMg_rho':0.5,
            'MgMg_C':0.0,
            'MgMg_cutoff':12.0,
            'MgO_A':821.6,
            'MgO_rho':0.3242,
            'MgO_C':0.0,
            'MgO_cutoff':12.0,
            'OO_A':2274.00,
            'OO_rho':0.1490,
            'OO_C':27.88,
            'OO_cutoff':12.0
            }
        }
    }

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

def test__LammpsStructuralMinimization____init____conditions():
    o = LammpsStructuralMinimization(**init_kwargs)
    assert isinstance(o.conditions, dict)
    assert isinstance(o.conditions_INIT, dict)
    assert isinstance(o.conditions_CONFIG, dict)
    assert isinstance(o.conditions_RUNNING, dict)
    assert isinstance(o.conditions_READY, dict)
    assert isinstance(o.conditions_POST, dict)
    assert isinstance(o.conditions_FINISHED, dict)
    assert isinstance(o.conditions_ERROR, dict)

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
    o.configure_potential(potential=configuration['potential'])
    assert isinstance(o.potential,
                      expected_values['potential']['potential_type'])
    cleanup()

def test__lammps_input_file_to_string():
    from mexm.manager import PotentialManager
    o = LammpsStructuralMinimization(**init_kwargs)
    o.configure_potential(potential=configuration['potential'])
    assert isinstance(o.lammps_input_file_to_string(), str)
    cleanup()

def dev__LammpsStructuralMinimization__on_init():
    o = LammpsStructuralMinimization(**init_kwargs)
    o.on_init(configuration)
    o.on_config(configuration)
    o.on_ready(configuration)
    while o.status != 'POST':
        o.update_status()
    o.on_post(configuration)
    print(o.configuration)
    print(o.results)

if __name__ == '__main__':
   dev__LammpsStructuralMinimization__on_init()
