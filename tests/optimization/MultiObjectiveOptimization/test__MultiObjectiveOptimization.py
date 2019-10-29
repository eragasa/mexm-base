import pytest
from collections import OrderedDict
from mexm.optimization import MultiObjectiveOptimization

def dev____init__():
    moo = MultiObjectiveOptimization()

def test____init__():
    moo = MultiObjectiveOptimization()
    assert isinstance(moo.design_variables, OrderedDict)
    assert isinstance(moo.objective_variables, OrderedDict)
    assert isinstance(moo.additional_design_constraints, list)
    assert isinstance(moo.additional_objective_constraints, list)\

def dev__add_design_variable():
    moo = MultiObjectiveOptimization()
    moo.add_design_variable(name='design_1')
    moo.add_design_variable(name='design_2')
    moo.add_design_variable(name='design_2',
                            constraints=[
                                ['<',1.0],
                                ['>',0.0]
                            ])
    moo.add_design_variable(name='design_3',
                            constraints=[
                                ['=',0.0]
                            ])
    print(moo.design_variables)

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

def dev__add_objective_variable():
    moo = MultiObjectiveOptimization()
    moo.add_objective_variable(name='obj_1',
                               optimization_type='min'
                               )
    moo.add_objective_variable(name='obj_2',
                               optimization_type='max'
                               )
    print(moo.objective_variables)


def test__add_objective_variable__type_min():
    obj_var_name = 'obj_1'
    obj_opt_type = 'min'
    obj_constraints = []
    moo = MultiObjectiveOptimization()
    moo.add_objective_variable(name=obj_var_name,
                               optimization_type=obj_opt_type)

    assert isinstance(moo.objective_variables, OrderedDict)
    assert obj_var_name in moo.objective_variables
    assert moo.objective_variables[obj_var_name]['optimization_type'] \
         == obj_opt_type
    assert moo.objective_variables[obj_var_name]['constraints'] \
         == obj_constraints

def test__add_objective_variable__type_max():
    obj_var_name = 'obj_2'
    obj_opt_type = 'max'
    obj_constraints = []
    moo = MultiObjectiveOptimization()
    moo.add_objective_variable(name=obj_var_name,
                               optimization_type=obj_opt_type)

    assert isinstance(moo.objective_variables, OrderedDict)
    assert obj_var_name in moo.objective_variables
    assert moo.objective_variables[obj_var_name]['optimization_type'] \
         == obj_opt_type
    assert moo.objective_variables[obj_var_name]['constraints'] \
         == obj_constraints

def test__add_objective_variable__type_invalid():
    obj_var_name = 'obj_2'
    obj_opt_type = 'invalid'
    obj_constraints = []
    moo = MultiObjectiveOptimization()

    with pytest.raises(AssertionError):
        moo.add_objective_variable(name=obj_var_name,
                                   optimization_type=obj_opt_type)

def dev__add_objective_variable():
    moo = MultiObjectiveOptimization()
    moo.add_objective_variable(name='obj_1',
                               optimization_type='min'
                               )
    moo.add_objective_variable(name='obj_2',
                               optimization_type='max'
                               )
    print(moo.objective_variables)
if __name__ == '__main__':
    dev____init__()
    dev__add_design_variable()
    dev__add_objective_variable()
    dev____str__()
