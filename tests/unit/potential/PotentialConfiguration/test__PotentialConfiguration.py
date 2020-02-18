import pytest
from collections import OrderedDict
from mexm.potential import PotentialConfiguration
from mexm.potential import BuckinghamPotential

def test____init__no_args():
    potential_configuration = PotentialConfiguration()
    assert potential_configuration.potential_type is None
    assert potential_configuration.symbols is None
    assert potential_configuration.parameters is None

def test__initialize_from_potential():
    symbols = ['Mg', 'O']
    potential = BuckinghamPotential(symbols)

    potential_configuration = PotentialConfiguration.initialize_from_potential(
        potential=potential
    )
    assert isinstance(potential_configuration, PotentialConfiguration)
    assert potential_configuration.potential_type == 'buckingham'
    assert potential_configuration.symbols == symbols
    assert any([
               potential_configuration.parameters is None,
               isinstance(potential_configuration.parameters, OrderedDict)
               ])

def test__potential_type__set_get():
    potential_type = 'buckingham'
    expected_potential_type = 'buckingham'
    potential_configuration = PotentialConfiguration()
    potential_configuration.potential_type = potential_type
    assert potential_configuration.potential_type == expected_potential_type

def test__symbols__set_get():
    symbols = ['Mg', 'O']
    potential_configuration = PotentialConfiguration()
    potential_configuration.symbols = symbols
    assert potential_configuration.symbols == symbols

def test__parameters__set_get():
    parameters = OrderedDict([
        ('A', 1.0), ('B', 2.0)
    ])
    potential_configuration = PotentialConfiguration()
    potential_configuration.parameters = parameters
    assert potential_configuration.parameters == parameters

def test__to_dict():
    potential_type = 'buckingham'
    symbols = ['Mg', 'O']
    parameters = OrderedDict([
        ('A', 1.0), ('B', 2.0)
    ])

    potential_configuration = PotentialConfiguration()
    potential_configuration.potential_type = potential_type
    potential_configuration.symbols = symbols
    potential_configuration.parameters = parameters

    expected_dict = OrderedDict()
    expected_dict['potential_type'] = potential_type
    expected_dict['symbols'] = symbols
    expected_dict['parameters'] = parameters

    assert isinstance(potential_configuration.to_dict(), OrderedDict)
    assert potential_configuration.to_dict() == expected_dict

def dev__to_dict():
    potential_type = 'buckingham'
    symbols = ['Mg', 'O']
    parameters = OrderedDict([
        ('A', 1.0), ('B', 2.0)
    ])

    potential_configuration = PotentialConfiguration()
    potential_configuration.potential_type = potential_type
    potential_configuration.symbols = symbols
    potential_configuration.parameters = parameters

    print(potential_configuration.to_dict())

if __name__ == "__main__":
   dev__to_dict()
