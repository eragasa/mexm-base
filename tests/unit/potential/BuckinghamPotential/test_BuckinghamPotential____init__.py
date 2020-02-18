import pytest
from collections import OrderedDict
from mexm.potential import BuckinghamPotential

def test____init____no_args():
    symbols = ['Mg', 'O']

    potential = BuckinghamPotential(symbols=symbols)

    assert isinstance(potential.parameter_names, list)
    assert isinstance(potential.parameters, OrderedDict)

def dev____init____no_args():
    symbols = ['Mg', 'O']
    potential = BuckinghamPotential(symbols=symbols)
    print('parameter_names')
    for pn in potential.parameter_names:
        print('\t{}'.format(pn))

    print('parameters')
    for k,v in potential.parameters.items():
        print('\t{}:{}'.format(k,v))

if __name__ == "__main__":
    dev____init____no_args()
