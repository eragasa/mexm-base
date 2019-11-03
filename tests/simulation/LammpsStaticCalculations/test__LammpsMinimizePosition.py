import pytest
import os, shutil
from collections import OrderedDict
from mexm.structure import SimulationCell
from mexm.simulation import LammpsStaticCalculation
from mexm.potential import BuckinghamPotential

resources_dir = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..',
        '..',
        'resources'))
structure_dir = os.path.join(resources_dir,'MgO_structures')

init_kwargs = {
    'name':'test_name',
    'simulation_path':'simulation_path',
    'structure_path': os.path.join(structure_dir, 'MgO_NaCl_333_fr_a.vasp'),
    'bulk_structure_name':'MgO_NaCl_unit'
}

configuration = {
    'simulation':{
        'simulation_type':'lammps_min_all'
        'name':'MgO_NaCl.lammps_min_pos',
        'simulation_path':'MgO_NaCl_333_fr_a.lammps_min_pos'
    },
    'structures':{
        'structure_name':'MgO_NaCl_333_fr_a',
        'structure_path':os.path.join(structure_dir, 'MgO_NaCl_333.fr_a.vasp'),
        'bulk_structure_name':'MgO_NaCl_unit.vasp'
    },
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

def test__LammpsStaticCalculation__properties():
    assert LammpsStaticCalculation.simulation_type == 'lammps_min_none'
    assert LammpsStaticCalculation.is_base_class == False

def test__LammpsStaticCalculation__inheritance():
    o = LammpsStaticCalculation(**init_kwargs)
    from mexm.simulation import LammpsSimulation
    assert isinstance(o, LammpsSimulation)

    from mexm.simulation import StaticCalculation
    assert isinstance(o, StaticCalculation)

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
    cleanup()

def test__LammpsStaticCalculation____init__():
    o = LammpsStaticCalculation(**init_kwargs)
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

def test__LammpsStaticCalculation____init____update_status():
    o = LammpsStaticCalculation(**init_kwargs)
    o.is_fullauto = False
    o.update_status()
    assert o.status == 'INIT'

def test__configure_potential__w_dict():
    o = LammpsStaticCalculation(**init_kwargs)
    o.configure_potential(potential=potential_config)
    assert isinstance(o.potential,
                      expected_values['potential']['potential_type'])
    cleanup()

def test__LammpsStructuralMinimization__on_init():
    o = LammpsStructuralMinimization(**init_kwargs)
    o.is_fullauto = False
    o.update_status()
    print(o.conditions_INIT)
    print(all([v for k,v in o.conditions_INIT.items()]))
    assert o.status == 'INIT'
    o.on_init(configuration)
    assert o.status == 'CONFIG'
    cleanup()


def test__lammps_input_file_to_string():
    from mexm.manager import PotentialManager
    o = LammpsStaticCalculation(**init_kwargs)
    o.configure_potential(potential=potential_config)
    assert isinstance(o.lammps_input_file_to_string(), str)
    cleanup()

def dev__lammps_input_file_to_string():
    o = LammpsStaticCalculation(**init_kwargs)
    o.configure_potential(potential=potential_config)
    print(o.lammps_input_file_to_string())
    cleanup()

def dev__set_potential_parameters():
    o = LammpsStaticCalculation(**init_kwargs)
    o.configure_potential(potential=potential_config)
    o.set_potential_parameters()

if __name__ == "__main__":
    dev__lammps_input_file_to_string()
