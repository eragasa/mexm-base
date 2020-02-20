import pytest

import os
from collections import namedtuple
from mexm.simulation import Simulation

parent_path = os.path.dirname(os.path.realpath(__file__))
SimulationArguments = namedtuple('SimulationArguments',
                                 ['name','path'])

@pytest.fixture
def simulation_args():
    name = 'test_name'
    path = 'test_path'
    return SimulationArguments(name, path)

@pytest.fixture
def simulation_obj(simulation_args):
    return Simulation(name = simulation_args.name,
                      path = simulation_args.path)

def test___init___(simulation_args, simulation_obj):
    obj = simulation_obj
    # property: name
    assert obj.name == simulation_args.name

    # property: path
    assert os.path.isabs(obj.path)
    if os.path.isabs(simulation_args.path):
        assert obj.path == simulation_args.path
    else:
        assert obj.path == os.path.abspath(simulation_args.path)

    # atttribute: conditions
    for state in Simulation.states:
        assert state in obj.conditions
        assert isinstance(obj.conditions[state], dict)

    # property: conditions_INIT:
    assert isinstance(obj.conditions_INIT, dict)
    assert isinstance(obj.conditions_CONFIG, dict)
    assert isinstance(obj.conditions_READY, dict)
    assert isinstance(obj.conditions_RUNNING, dict)
    assert isinstance(obj.conditions_POST, dict)
    assert isinstance(obj.conditions_FINISHED, dict)
    assert isinstance(obj.conditions_ERROR, dict)

def test_run(simulation_obj):
    obj = simulation_obj

    with pytest.raises(NotImplementedError):
        obj.run()

if __name__ == "__main__":
    pass
