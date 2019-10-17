import pytest
from collections import OrderedDict
from moo import MultiObjectiveOptimization

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
    moo.add_design_variable(name='design_1',
                            constraints=['>',0])
    moo.add_design_variable(name='design_2')
    moo.add_objective_variable(name='optimization_1',
                               optimization_type='min',
                               constraints=['>',0]
                               )
    print(moo)

if __name__ == '__main__':
    dev____init__()
    dev__add_design_variable()
    dev__add_objective_variable()
