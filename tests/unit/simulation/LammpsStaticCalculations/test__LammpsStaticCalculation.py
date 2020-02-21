import pytest
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
def init_kwargs(configuration_dict):
    kwargs = {
        'name':configuration_dict['simulation']['path'],
        'simulation_path':configuration_dict['simulation']['path'],
        'structure_path':configuration_dict['structures']['path'],
        'bulk_structure_name':configuration_dict['simulation']['bulk_name']
    }
    return kwargs

@pytest.fixture
def configuration_dict(resourcedir):

    configuration = {}

    simulation_name = 'MgO_NaCl.lmps_min_none'
    simulation_path = os.path.join(str(resourcedir),simulation_name)
    configuration['simulation'] = {
        'name':simulation_name,
        'path':simulation_path,
        'bulk_name':None
    }

    structure_name = 'MgO_NaCl_unit'
    structure_path = os.path.join(str(resourcedir),'MgO_NaCl_unit.vasp')
    configuration['structures'] = {
        'name':structure_name,
        'path':structure_path
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

results = {
    'MgO_NaCl_unit.lmps_min_all.a0':4.00
}

@pytest.fixture
def expected_values_dict():
    expected_values = {
        'potential':{
            'potential_name':'buckingham',
            'potential_type':BuckinghamPotential
        }
    }
    return expected_values

@pytest.fixture
def expected_static_variables():
    static_variables ={
        'simulation_type':'lammps_min_none',
        'is_base_class':False
    }
    return static_variables

def test_static_variables(
    expected_static_variables
    ):
    """ testing static attributes

    Args:
        expected_static_variables (dict): this is a testing fixture
    """
    assert LammpsStaticCalculation.simulation_type == expected_static_variables['simulation_type']
    assert LammpsStaticCalculation.is_base_class == expected_static_variables['is_base_class']
    
def test_inheritance(
        resourcedir,
        init_kwargs
):

    o = LammpsStaticCalculation(**init_kwargs)
    assert isinstance(o, LammpsSimulation)
    assert isinstance(o, StaticCalculation)

def test___init____conditions(
        resourcedir,
        init_kwargs):
    """ test to see of all the dictionaries are setup correctly """

    o = LammpsStaticCalculation(**init_kwargs)
    assert isinstance(o.conditions, dict)
    assert isinstance(o.conditions_INIT, dict)
    assert isinstance(o.conditions_CONFIG, dict)
    assert isinstance(o.conditions_RUNNING, dict)
    assert isinstance(o.conditions_READY, dict)
    assert isinstance(o.conditions_POST, dict)
    assert isinstance(o.conditions_FINISHED, dict)
    assert isinstance(o.conditions_ERROR, dict)

def test___init__default(
        resourcedir,
        init_kwargs
    ):
    """ testing the default constructor
    
    Args:
        resourcedir: this is fixture which provides a temp filesystem
        init_kwargs (dict): this is a testing fixture
    """

    o = LammpsStaticCalculation(**init_kwargs)

    assert not o.is_fullauto
    assert o.potential is None
    assert o.lammps_script is None

    assert o.structure_path == init_kwargs['structure_path']
    assert isinstance(o.structure, SimulationCell)
    assert o.bulk_structure_name == init_kwargs['bulk_structure_name']

    assert o.lammps_input_path == os.path.join(init_kwargs['simulation_path'], 'lammps.in')
    assert o.lammps_output_path == os.path.join(init_kwargs['simulation_path'], 'lammps.out')
    assert o.lammps_structure_path == os.path.join(init_kwargs['simulation_path'], 'lammps.structure')
    assert o.lammps_potentialmod_path == os.path.join(init_kwargs['simulation_path'], 'potential.mod')
    assert o.lammps_setfl_path is None

    assert o.use_mpi == False
    if 'LAMMPS_SERIAL_BIN' in os.environ:
        assert o.lammps_bin == os.environ['LAMMPS_SERIAL_BIN']
    else:
        assert o.lammps_bin is None

    # the path should have been created
    assert os.path.isdir(init_kwargs['simulation_path'])

    # the status should be INIT
    assert o.status == 'INIT'

def test__configure_potential__w_dict(
        resourcedir,
        init_kwargs,
        configuration_dict,
        expected_values_dict
    ):
    """ testing the potential configuration
    
    Args:
        resourcedir: this is fixture which provides a temp filesystem
        init_kwargs (dict): this is a testing fixture
        configuration_dict (dict): this is a testing fixture
        expected_values_dict (dict):  this is a testing fixture
    """

    # this is the setup for the test
    o = LammpsStaticCalculation(**init_kwargs)
    o.configure_potential(potential=configuration_dict['potential'])

    # check to see if the potential are the correct type
    assert isinstance(
        o.potential,
        expected_values_dict['potential']['potential_type']
    )

def test__on_init(
        resourcedir,
        init_kwargs,
        configuration_dict,
        expected_values_dict
    ):
    """ testing on_init
    
    Args:
        resourcedir: this is fixture which provides a temp filesystem
        init_kwargs (dict): this is a testing fixture
        configuration_dict (dict): this is a testing fixture
        expected_values_dict (dict):  this is a testing fixture
    """
    o = LammpsStaticCalculation(**init_kwargs)
    o.on_init(configuration_dict)

    for k,v in o.conditions_CONFIG.items():
        print(k, v)
    assert o.status == 'CONFIG'

def test__on_config(
    resourcedir,
    init_kwargs,
    configuration_dict,
    expected_values_dict
):
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

    o.update_status()
    for k,v in o.conditions_READY.items():
        print(k, v)
    assert o.status == 'READY'

def test__modify_structure_file(
    resourcedir,
    init_kwargs,
    configuration_dict,
    expected_values_dict
):
    """ testing on_config
    
    Args:
        resourcedir: this is fixture which provides a temp filesystem
        init_kwargs (dict): this is a testing fixture
        configuration_dict (dict): this is a testing fixture
        expected_values_dict (dict):  this is a testing fixture
    """

    from copy import deepcopy
    init_kwargs_ = deepcopy(init_kwargs)
    init_kwargs_['bulk_structure_name'] = 'MgO_NaCl_unit'
    print(init_kwargs_)
    o = LammpsStaticCalculation(**init_kwargs_)
    assert o.status == 'INIT'

    o.on_init(configuration_dict)
    o.update_status()
    assert o.status == 'INIT'

    # passing in an empty result should not move the status
    results = {}
    o.on_config(configuration_dict, results)
    o.update_status()
    assert o.status == 'INIT'

    # passing in a non empty result should move the status 
    results = {'MgO_NaCl_unit.lmps_min_all.a0':4.0}
    assert isinstance(o.results, dict)
    assert 'MgO_NaCl_unit.lmps_min_all.a0' not in o.results

    o.on_config(configuration_dict, results)
    o.update_status()
    assert o.status == 'READY'

@pytest.mark.skipif(os.name=='nt', reason='requires a POSIX subsystem')
def test__on_ready():
    o = LammpsStaticCalculation(**init_kwargs)
    o.is_fullauto = False
    o.update_status()
    o.on_init(configuration)
    o.on_config(configuration)
    assert o.status == 'READY'
    o.on_ready()
    assert os.path.isfile(o.lammps_structure_path)
    assert os.path.isfile(o.lammps_potentialmod_path)
    assert os.path.isfile(o.lammps_input_path)

    assert o.status == 'RUNNING'

@pytest.mark.skipif(
    os.environ.get('TRAVIS') == 1,
    reason = 'Requires LAMMPS to test'
)
@pytest.mark.skipif(os.name=='nt', reason='requires a POSIX subsystem')
def test__on_running(
        init_kwargs,
        configuration_dict
    ):
    o = LammpsStaticCalculation(**init_kwargs)
    o.is_fullauto = False
    o.update_status()
    o.on_init(configuration_dict)
    o.on_config(configuration_dict)
    o.on_ready()

    while o.status == 'RUNNING':
        o.update_status()
        o.on_running()
 
    assert o.status == 'POST'

def test__lammps_input_file_to_string(init_kwargs, configuration_dict):
    o = LammpsStaticCalculation(**init_kwargs)
    o.configure_potential(potential=configuration_dict['potential'])
    assert isinstance(o.lammps_input_file_to_string(), str)

if __name__ == "__main__":
    pass