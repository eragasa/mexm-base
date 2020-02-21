import pytest
from distutils import dir_util
import os, shutil
from collections import OrderedDict
from mexm.structure import SimulationCell
from mexm.simulation import LammpsNptSimulation
from mexm.simulation import LammpsSimulation
from mexm.simulation import NptSimulation
from mexm.potential import BuckinghamPotential

@pytest.fixture
def resourcedir(tmpdir, request):
    '''
    Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    '''
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir

@pytest.fixture
def configuration_dict(resourcedir):

    configuration = {}

    simulation_name = "MgO_NaCl.lammps_npt"
    simulation_path = os.path.join(str(resourcedir), simulation_name)
    configuration['simulation'] = {
        'name':simulation_name,
        'path':simulation_path,
        'bulk_name':None
    }

    configuration['npt'] = {
        'thermostat_type':'NoseHoover',
        'temperature_initial': 0.0, # in Kelvin
        'temperature_final': 100.0, # in Kelvin
        'temperature_damp': 'Auto',
        'pressure_initial': 0.0, # in Bars
        'pressure_final': 1000, # in Bars
        'pressure_damp':'Auto',
        'drag_coefficient':'Auto',
        'time_ramp':10000,
        'time_run':10000,
        'time_step':3 
    }

    structure_name = 'MgO_NaCl_unit'
    structure_path = os.path.join(str(resourcedir), 'MgO_NaCl_unit.vasp')
    structure_sc = [10,10,10]
    configuration['structures'] = {
        'name':structure_name,
        'path':structure_path,
        'supercell':structure_sc
    }

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

@pytest.fixture
def init_kwargs(configuration_dict):
    kwargs = {
        'name':configuration_dict['simulation']['name'],
        'simulation_path':configuration_dict['simulation']['path'],
        'structure_path':configuration_dict['structures']['path'],
        'bulk_structure_name':configuration_dict['simulation']['bulk_name']
    }
    return kwargs

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

@pytest.fixture
def expected_static_variables():
    static_variables = {
        'simulation_type':'lammps_npt',
        'is_base_class':False
    }
    return static_variables

def test__static_variables(
    expected_static_variables
):
    assert LammpsNptSimulation.simulation_type == expected_static_variables['simulation_type']
    assert LammpsNptSimulation.is_base_class == expected_static_variables['is_base_class']

def test____init__(
    init_kwargs,
    resourcedir
):
    print(init_kwargs)
    o = LammpsNptSimulation(**init_kwargs)
    assert isinstance(o, LammpsSimulation)
    assert isinstance(o, NptSimulation)

def test__inheritance(
    init_kwargs,
    resourcedir
):
    o = LammpsNptSimulation(**init_kwargs)
    assert isinstance(o, LammpsSimulation)
    assert isinstance(o, NptSimulation)
