import pytest
from potentialmanager import PotentialManager

def  dev__PotentialManager__get_potential_types():
    print(80*'-')
    print('{:80}'.format('PotentialManager.get_potential_types()'))
    print(80*'-')
    potential_types = PotentialManager.get_potential_types()


    for potential_type in potential_types:
        print(potential_type)

def dev__PotentialManager__get_potential_names():
    print(80*'-')
    print('{:80}'.format('PotentialManager.get_potential_names()'))
    print(80*'-')

    potential_names = PotentialManager.get_potential_names()

    for potential_name in potential_names:
        print(potential_name)


def dev__PotentialManager__get_potential_map():
    print(80*'-')
    print('{:80}'.format('PotentialManager.get_potential_map()'))
    print(80*'-')

    potential_map = PotentialManager.get_potential_map()

    for k, v in potential_map.items():
        print(k, v)
if __name__ == "__main__":
    dev__PotentialManager__get_potential_types()
    dev__PotentialManager__get_potential_names()
    dev__PotentialManager__get_potential_map()
