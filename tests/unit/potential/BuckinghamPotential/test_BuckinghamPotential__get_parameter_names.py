import pytest
from collections import OrderedDict
from mexm.potential import BuckinghamPotential

def dev__BuckinghamPotential__get_parameter_names():
    symbols = ['Mg', 'O']
    parameter_names = BuckinghamPotential.get_parameter_names(
            symbols=symbols,
            hybrid_format=False
    )
    print(parameter_names)

def test__BuckinghamPotentials__get_parameter_names__not_hybrid():
    symbols = ['Mg', 'O']
    expected_results = {
        'parameter_names':[
            'cutoff',
            'Mg_chrg', 'O_chrg',
            'MgMg_A', 'MgMg_rho', 'MgMg_C', 'MgMg_cutoff',
            'MgO_A', 'MgO_rho', 'MgO_C', 'MgO_cutoff',
            'OO_A', 'OO_rho', 'OO_C', 'OO_cutoff'
        ]
    }
    parameter_names = BuckinghamPotential.get_parameter_names(
            symbols=symbols,
            hybrid_format=False
    )
    assert isinstance(parameter_names, list)
    assert parameter_names == expected_results['parameter_names']

if __name__ == "__main__":
    symbols = ['Mg', 'O']
    parameter_names = BuckinghamPotential.get_parameter_names(
            symbols=symbols,
            hybrid_format=False
    )
    print(parameter_names)
