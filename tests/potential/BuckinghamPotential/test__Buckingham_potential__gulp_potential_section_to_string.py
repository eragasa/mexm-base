import pytest
from collections import OrderedDict
from mexm.potential import BuckinghamPotential
from mexm.potential.lewiscatlow1985 import LewisCatlow1985

def test__gulp_potential_section_to_string():
    symbols = ['Mg', 'O']

    parameters = OrderedDict()
    for k in BuckinghamPotential.get_parameter_names(symbols):
        try:
            parameters[k] = LewisCatlow1985['parameters'][k]
        except KeyError as e:
            parameters[k] = 12.0

    potential = BuckinghamPotential(symbols=symbols)
    s = potential.gulp_potential_section_to_string(parameters=parameters)
    assert isinstance(s, str)

def dev__gulp_potential_section_to_string():
    symbols = ['Mg', 'O']

    parameters = OrderedDict()
    for k in BuckinghamPotential.get_parameter_names(symbols):
        try:
            parameters[k] = LewisCatlow1985['parameters'][k]
        except KeyError as e:
            parameters[k] = 12.0

    potential = BuckinghamPotential(symbols=symbols)
    s = potential.gulp_potential_section_to_string(parameters=parameters)
    print(80*'-')
    print('{:^80}'.format('GULP POTENTIAL SECTION'))
    print(80*'-')
    print(s)

if __name__ == "__main__":
    dev__gulp_potential_section_to_string()