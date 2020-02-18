import pytest
from mexm.potential import BornMayerPotential

def test__BornMayerPotential____init____no_args():
    symbols = ['Ni', 'Al']
    potential = BornMayerPotential(symbols=symbols)

    assert isinstance(potential.parameter_names, list)
    assert isinstance(potential.parameters, dict)


def dev__BornMayerPotential____init____no_args():
    symbols = ['Ni', 'Al']
    potential = BornMayerPotential(symbols=symbols)

    print('parameter_names')
    for pn in potential.parameter_names:
        print('\t{}'.format(pn))

def test__BornMayerPotential__get_parameter_names():
    symbols = ['Ni', 'Al']
    expected_parameter_names = [
        'NiNi_phi0', 'NiNi_gamma', 'NiNi_r0', 'NiNi_rcut',
        'NiAl_phi0', 'NiAl_gamma', 'NiAl_r0', 'NiAl_rcut',
        'AlAl_phi0', 'AlAl_gamma', 'AlAl_r0', 'AlAl_rcut']
    parameter_names =  BornMayerPotential.get_parameter_names(symbols)
    assert isinstance(parameter_names, list)
    assert parameter_names == expected_parameter_names

def dev__BornMayerPotential__get_parameter_names():
    symbols = ['Ni', 'Al']
    parameter_names =  BornMayerPotential.get_parameter_names(symbols)
    print(parameter_names)

if __name__ == "__main__":
    dev__BornMayerPotential____init____no_args()
    dev__BornMayerPotential__get_parameter_names()
