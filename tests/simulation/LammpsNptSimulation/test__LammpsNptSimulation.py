import pytest
import os, shutil
from collections import OrderedDict
from mexm.structure import SimulationCell
from mexm.simulation import LammpsNptSimulation, LammpsSimulation
from mexm.potential import BuckinghamPotential

structure_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', '..', 'resources', 'MgO_structures')
structure_dir = os.path.abspath(structure_dir)
init_kwargs = {
    'name':'test_name',
    'simulation_path':'simulation_path',
    'structure_path':os.path.join(structure_dir,'MgO_NaCl_unit.vasp'),
    'bulk_structure_name':'MgO_unit_cell'
}

simulation_configuration = {
    'name',
    'simulation_path',
    'structure_path',
    'bulk_structure_name',
    'temperature_initial',
    'temperature_final',
    'temperature_damp',
    'pressure_initial',
    'pressure_final',
    'pressure_damp',
    'drag_coefficient',
    'time_ramp',
    'time_run',
    'time_step'
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

def test__LammpsNptSimulation__inheritance():
    o = LammpsNptSimulation(**init_kwargs)
    from mexm.simulation import LammpsSimulation
    assert isinstance(o, LammpsSimulation)

    from mexm.simulation import NptSimulation
    assert isinstance(o, NptSimulation)