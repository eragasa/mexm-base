import pytest
from mexm.potential import EamEmbeddingFunction
from mexm.potential import UniversalEmbeddingFunction
from mexm.manager import PotentialManager
class_potential = UniversalEmbeddingFunction
symbols = ['Ni', 'Al']
expected_values = {
    'potential_type':'eamembed_universal',
    'is_base_potential':False,
    'parameter_names':[
        'Ni_F0', 'Ni_p', 'Ni_q', 'Ni_F1', 'Ni_rho0', 'Ni_rhocut',
        'Al_F0', 'Al_p', 'Al_q', 'Al_F1', 'Al_rho0', 'Al_rhocut']
}

def dev__UniversalEmbeddingFunction__properties():
    print(UniversalEmbeddingFunction.potential_type)

def test__UniversalEmbeddingFunction__properties():
    assert class_potential.potential_type == expected_values['potential_type']
    assert class_potential.is_base_potential == expected_values['is_base_potential']

def test__UniversalEmbeddingFunction__PotentialManager():
    potential_type = class_potential.potential_type
    potential_type in [k.potential_type for k in PotentialManager.get_potential_types()]

def dev__UniversalEmbeddingFunction__get_parameter_names():
    print(class_potential.get_parameter_names(symbols=symbols))

def test__UniversalEmbeddingFunction____init__():
    o = class_potential(symbols=symbols)
    assert isinstance(o, EamEmbeddingFunction)
    assert isinstance(o.parameter_names, list)
    assert isinstance(o.parameters, dict)

if __name__ == "__main__":
    dev__UniversalEmbeddingFunction__properties()
    dev__UniversalEmbeddingFunction__get_parameter_names()
