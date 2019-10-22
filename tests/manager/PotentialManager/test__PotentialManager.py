import pytest
from collections import OrderedDict
from mexm.manager import PotentialManager

def dev__PotentialManager__get_potential_types():
    print(80*'-')
    print('{:80}'.format('PotentialManager.get_potential_types()'))
    print(80*'-')
    potential_types = PotentialManager.get_potential_types()

    for potential_type in potential_types:
        print(potential_type)

def test__PotentialManager__get_potential_type():
    potential_types = PotentialManager.get_potential_types()
    assert isinstance(potential_types, list)

def dev__PotentialManager__get_potential_names():
    print(80*'-')
    print('{:80}'.format('PotentialManager.get_potential_names()'))
    print(80*'-')

    potential_names = PotentialManager.get_potential_names()

    for potential_name in potential_names:
        print(potential_name)

def test__PotentialManager__get_potential_names():
    potential_names = PotentialManager.get_potential_names()
    assert isinstance(potential_names, list)

def dev__PotentialManager__get_potential_map():
    print(80*'-')
    print('{:80}'.format('PotentialManager.get_potential_map()'))
    print(80*'-')

    potential_map = PotentialManager.get_potential_map()

    for k, v in potential_map.items():
        print(k, v)

def test__PotentialManager__get_potential_map():
    potential_map = PotentialManager.get_potential_map()
    isinstance(potential_map, OrderedDict)
if __name__ == "__main__":
    dev__PotentialManager__get_potential_types()
    dev__PotentialManager__get_potential_names()
    dev__PotentialManager__get_potential_map()
