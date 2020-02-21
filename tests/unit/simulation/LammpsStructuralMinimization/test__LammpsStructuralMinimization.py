import pytest
from distutils import dir_util

import os, shutil
from collections import OrderedDict
from mexm.structure import SimulationCell
from mexm.potential import BuckinghamPotential
from mexm.simulation import LammpsSimulation
from mexm.simulation import StructuralMinimization
from mexm.simulation import LammpsStructuralMinimization

parent_path = os.path.dirname(os.path.abspath(__file__))
@pytest.fixture
def resourcedir(tmpdir, request):
    '''
    Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    https://stackoverflow.com/questions/29627341/pytest-where-to-store-expected-data
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
        'bulk_structure_name':None
    }
    return kwargs

@pytest.fixture
def configuration_dict(resourcedir):

    configuration = {}

    simulation_name = 'MgO_NaCl.lmps_min_all'
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

@pytest.fixture
def expected_values_dict():
    expected_values = {
        'potential':{
            'potential_name':'buckingham',
            'potential_type':BuckinghamPotential
        }
    }

    return expected_values

def test_properties():
    assert LammpsStructuralMinimization.simulation_type == 'lammps_min_all'
    assert LammpsStructuralMinimization.is_base_class == False

def dev____init__(resourcedir, init_kwargs):
    o = LammpsStructuralMinimization(**init_kwargs)
    assert os.path.isdir(init_kwargs.simulation_path)

def dev___init___inheritance(resourcedir, init_kwargs):
    o = LammpsStructuralMinimization(**init_kwargs)
    assert isinstance(o, LammpsSimulation)
    assert isinstance(o, StructuralMinimization)

def test___init___conditions(init_kwargs, resourcedir):
    o = LammpsStructuralMinimization(**init_kwargs)
    assert isinstance(o.conditions, dict)
    assert isinstance(o.conditions_INIT, dict)
    assert isinstance(o.conditions_CONFIG, dict)
    assert isinstance(o.conditions_RUNNING, dict)
    assert isinstance(o.conditions_READY, dict)
    assert isinstance(o.conditions_POST, dict)
    assert isinstance(o.conditions_FINISHED, dict)
    assert isinstance(o.conditions_ERROR, dict)

def test___init__(
        init_kwargs, 
        resourcedir
    ):
    """ testing the default constructor 
    
    Args:
        init_kwargs: this is a testing fixture
        resourcedir: this is a testing fixture
    """

    o = LammpsStructuralMinimization(**init_kwargs)

    assert not o.is_fullauto
    assert o.potential is None
    assert o.lammps_script is None
    assert o.structure_path == init_kwargs['structure_path']
    assert isinstance(o.structure, SimulationCell)
    assert o.bulk_structure_name == init_kwargs['bulk_structure_name']

    assert o.lammps_input_path == os.path.join(init_kwargs['simulation_path'],'lammps.in')
    assert o.lammps_output_path == os.path.join(init_kwargs['simulation_path'],'lammps.out')
    assert o.lammps_structure_path == os.path.join(init_kwargs['simulation_path'],'lammps.structure')
    assert o.lammps_potentialmod_path == os.path.join(init_kwargs['simulation_path'],'potential.mod')
    assert o.lammps_setfl_path is None

    assert o.use_mpi == False
    if 'LAMMPS_SERIAL_BIN' in os.environ:
        assert o.lammps_bin == os.environ['LAMMPS_SERIAL_BIN']
    else:
        assert o.lammps_bin == os.environ['LAMMPS_SERIAL_BIN']
    except KeyError:
        assert o.lammps_bin is None

    # the path should have been created
    assert os.path.isdir(init_kwargs['simulation_path'])

def test__configure_potential__w_dict(
        init_kwargs,
        configuration_dict,
        expected_values_dict, 
        resourcedir
    ):
    """ testing the potential configuration
    
    Args:
        resourcedir: this is fixture which provides a temp filesystem
        init_kwargs (dict): this is a testing fixture
        configuration_dict (dict): this is a testing fixture
        expected_values_dict (dict):  this is a testing fixture
    """

    # this is the setup for the test
    o = LammpsStructuralMinimization(**init_kwargs)
    o.configure_potential(potential=configuration_dict['potential'])

    # check to see if the potential are the correct type
    assert isinstance(
        o.potential,
        expected_values_dict['potential']['potential_type']
    )

def test__lammps_input_file_to_string(
        init_kwargs,
        configuration_dict,
        resourcedir):

    configuration = configuration_dict

    o = LammpsStructuralMinimization(**init_kwargs)
    o.configure_potential(potential=configuration['potential'])
    assert isinstance(o.lammps_input_file_to_string(), str)

def test__on_init(
        init_kwargs,
        configuration_dict,
        resourcedir):

    configuration = configuration_dict

    o = LammpsStructuralMinimization(**init_kwargs)
    o.is_fullauto = False
    o.update_status()

    print(o.conditions_INIT)
    print(all([v for k,v in o.conditions_INIT.items()]))

    assert o.status == 'INIT'
    o.on_init(configuration)
    assert o.status == 'CONFIG'

@pytest.mark.skipif(os.name=='nt', reason='requires a POSIX subsystem')
def test__on_config(init_kwargs, resourcedir):
    o = LammpsStructuralMinimization(**init_kwargs)
    o.is_fullauto = False
    o.update_status()
    o.on_init(configuration)
    assert o.status == 'CONFIG'
    o.on_config(configuration)
    assert o.status == 'READY'
    cleanup()

@pytest.mark.skipif(os.name=='nt', reason='requires a POSIX subsystem')
def test__LammpsStructuralMinimization__on_ready():
    o = LammpsStructuralMinimization(**init_kwargs)
    o.is_fullauto = False
    o.update_status()
    o.on_init(configuration)
    o.on_config(configuration)
    assert o.status == 'READY'
    o.on_ready()
    assert o.status == 'RUNNING'
    cleanup()

@pytest.mark.skipif(os.name=='nt', reason='requires a POSIX subsystem')
def test__LammpsStructuralMinimization__on_running():
    o = LammpsStructuralMinimization(**init_kwargs)
    o.is_fullauto = False
    o.update_status()
    o.on_init(configuration)
    o.on_config(configuration)
    o.on_ready()
    while o.status == 'RUNNING':
        o.update_status()
        o.on_running()
    assert o.status == 'POST'
    cleanup()

def dev__LammpsStructuralMinimization__on_init():
    o = LammpsStructuralMinimization(**init_kwargs)
    o.is_fullauto = False
    o.on_init(configuration)
    o.on_config(configuration)
    o.on_ready(configuration)
    while o.status != 'POST':
        o.update_status()
    o.on_post(configuration)
    print(o.configuration)
    print(o.results)
    cleanup()

if __name__ == '__main__':
   dev__LammpsStructuralMinimization__on_init()
