
from distutils import dir_util

import os
import shutil
from collections import OrderedDict

from mexm.simulation import LammpsSimulation
from mexm.simulation import StaticCalculation
from mexm.simulation import LammpsStaticCalculation

from mexm.structure import SimulationCell
from mexm.potential import BuckinghamPotential

parent_path = os.path.dirname(os.path.abspath(__file__))
resources_path = os.path.join(parent_path,'test__LammpsStaticCalculation')

def configuration_dict():

    configuration = {}

    simulation_name = 'MgO_NaCl.lmps_min_none'
    simulation_path = os.path.join(parent_path, simulation_name)
    configuration['simulation'] = {
        'name':simulation_name,
        'path':simulation_path,
        'bulk_name':None
    }

    structure_name = 'MgO_NaCl_unit'
    structure_path = os.path.join(resources_path, 'MgO_NaCl_unit.vasp')
    configuration['structures'] = {}
    configuration['structures']['name'] = structure_name
    configuration['structures']['path'] = structure_path

    potential_name = 'buckingham'
    potential_symbols = ['Mg', 'O']
    potential_parameters = {
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
    configuration['potential'] = {
        'name':potential_name,
        'symbols':potential_symbols,
        'parameters':potential_parameters
    }

    return configuration

def init_kwargs(configuration_dict):
    kwargs = {
        'name':'test_name',
        'simulation_path':'MgO_NaCl_333_fr_a.lammps_min_none',
        'structure_path': configuration_dict['simulation']['path'],
        'bulk_structure_name':'MgO_NaCl_unit'
    }

    kwargs = {
        'name':configuration_dict['simulation']['path'],
        'simulation_path':configuration_dict['simulation']['path'],
        'structure_path':configuration_dict['structures']['path'],
        'bulk_structure_name':configuration_dict['simulation']['bulk_name']
    }
    return kwargs


results = {
    'MgO_NaCl_unit.lmps_min_all.a0':4.00
}

def expected_values_dict():
    expected_values = {
        'potential':{
            'potential_name':'buckingham',
            'potential_type':BuckinghamPotential
        }
    }
    return expected_values

def expected_static_variables():
    static_variables ={
        'simulation_type':'lammps_min_none',
        'is_base_class':False
    }
    return static_variables

def dev__on_config(init_kwargs, configuration_dict):
    """ testing on_config
    
    Args:
        resourcedir: this is fixture which provides a temp filesystem
        init_kwargs (dict): this is a testing fixture
        configuration_dict (dict): this is a testing fixture
        expected_values_dict (dict):  this is a testing fixture
    """
    o = LammpsStaticCalculation(**init_kwargs)
    o.on_init(configuration_dict)
    o.on_config(configuration_dict, results)
    assert isinstance(o.results, dict)

    if o.bulk_structure_name is not None:
        bulk_lattice_parameter_name = ".".join(
            o.bulk_structure_name,
            'lmps_min_all',
            'a0'
        )
        assert bulk_lattice_parameter_name in o.results

    assert os.path.isfile(o.lammps_structure_path)
    assert os.path.isfile(o.lammps_potentialmod_path)
    assert os.path.isfile(o.lammps_input_path)

    o.update_status()
    for k,v in o.conditions_READY.items():
        print(k, v)
    assert o.status == 'READY'

if __name__ == "__main__":
    dev__on_config(
        init_kwargs(configuration_dict=configuration_dict()),
        configuration_dict=configuration_dict()
    )