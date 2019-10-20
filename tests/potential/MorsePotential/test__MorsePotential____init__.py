import pytest
from collections import OrderedDict
from mexm.potential import MorsePotential

def test____init____no_args():
    symbols = ['Ni', 'Al']

    potential = MorsePotential(symbols=symbols)

    assert isinstance(potential.parameter_names, list)
    assert isinstance(potential.parameters, OrderedDict)

def dev____init____no_args():
    symbols = ['Ni', 'Al']

    potential = MorsePotential(symbols=symbols)

    print('parameter_names')
    for pn in potential.parameter_names:
        print('\t{}'.format(pn))

if __name__ == "__main__":
    dev____init____no_args()
