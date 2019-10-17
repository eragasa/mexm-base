import pytest
from collections import OrderedDict
from moo import MultiObjectiveOptimization

def dev____init__():
    moo = MultiObjectiveOptimization()

def test____init__():
    moo = MultiObjectiveOptimization()
    assert isinstance(moo.design_variables, OrderedDict)
    assert isinstance(moo.objective_variables, OrderedDict)
    assert isinstance(moo.additional_design_constraints, list)
    assert isinstance(moo.additional_objective_constraints, list)\


def dev____str__():
    moo = MultiObjectiveOptimization()
    moo.add_design_variable(
                        name='design_1',
                        constraints=[['>',0]]
                        )
    moo.add_design_variable(name='design_2')
    moo.add_objective_variable(
                        name='optimization_1',
                        optimization_type='min',
                        constraints=[['>',0]]
                        )
    print(moo)

if __name__ == '__main__':
    dev____init__()
    dev____str__()
