import pytest
from mexm.potential import EamPotential

def test__EamPotential__static_values():
    assert EamPotential.potential_type == 'eam'
    assert EamPotential.is_base_potential == False
    assert EamPotential.is_charge == False

def dev__EamPotential__get_parameter_names():
    kwargs = {
        'symbols':['Ni', 'Al'],
        'pair_type':'bornmayer',
        'density_type':'eamdens_exp',
        'embedding_type':'eamembed_universal'
    }
    parameter_names = EamPotential.get_parameter_names(**kwargs)
    print(parameter_names)
if __name__ == "__main__":
    dev__EamPotential__get_parameter_names()
