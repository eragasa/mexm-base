import pytest
import os
from mexm.task import Task

@pytest.fixture
def task_args():
    args = {
        'name':'task_name',
        'simulation_type':'vasp',
        'simulation_path':'test_path',
        'n_cores':40,
        'n_nodes':1
    }
    return args

@pytest.fixture
def objTask(task_args):
    task = Task(**task_args)
    return task
    
def test_init(task_args):
    objTask = Task(**task_args)
    assert objTask.name == task_args['name']
    assert objTask.simulation_type == task_args['simulation_type']
    assert os.path.isabs(objTask.simulation_path)
    assert objTask.simulation_path == task_args['simulation_path']
    assert objTask.n_cores == task_args['n_cores']
    assert objTask.n_nodes == task_args['n_nodes']


