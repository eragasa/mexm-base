import pytest
from mexm.potential import (PairPotential,
                            EamDensityFunction,
                            EamEmbeddingFunction,
                            EamPotential)

expected_values = {
    'parameter_names':[
        'rhocut', 'rcut',
        'pair_NiNi_phi0', 'pair_NiNi_gamma', 'pair_NiNi_r0', 'pair_NiNi_rcut',
        'pair_NiAl_phi0', 'pair_NiAl_gamma', 'pair_NiAl_r0', 'pair_NiAl_rcut',
        'pair_AlAl_phi0', 'pair_AlAl_gamma', 'pair_AlAl_r0', 'pair_AlAl_rcut',
        'dens_Ni_rho0', 'dens_Ni_beta', 'dens_Ni_r0', 'dens_Ni_cutoff',
        'dens_Al_rho0', 'dens_Al_beta', 'dens_Al_r0', 'dens_Al_cutoff',
        'embed_Ni_F0', 'embed_Ni_p', 'embed_Ni_q',
        'embed_Ni_F1', 'embed_Ni_rho0', 'embed_Ni_rhocut',
        'embed_Al_F0', 'embed_Al_p', 'embed_Al_q',
        'embed_Al_F1', 'embed_Al_rho0', 'embed_Al_rhocut']
}
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

def test__EamPotential__get_parameter_names():
    kwargs = {
        'symbols':['Ni', 'Al'],
        'pair_type':'bornmayer',
        'density_type':'eamdens_exp',
        'embedding_type':'eamembed_universal'
    }
    parameter_names = EamPotential.get_parameter_names(**kwargs)
    assert parameter_names == expected_values['parameter_names']

def test__EamPotential____init__():
    kwargs = {
        'symbols':['Ni', 'Al'],
        'pair_type':'bornmayer',
        'density_type':'eamdens_exp',
        'embedding_type':'eamembed_universal'
    }
    o = EamPotential(**kwargs)
    assert o.parameter_names == expected_values['parameter_names']
    assert o.pair['type'] == kwargs['pair_type']
    assert o.density['type'] == kwargs['density_type']
    assert o.embedding['type'] == kwargs['embedding_type']
    assert isinstance(o.pair['obj'], PairPotential)
    assert isinstance(o.density['obj'], EamDensityFunction)
    assert isinstance(o.embedding['obj'], EamEmbeddingFunction)
if __name__ == "__main__":
    dev__EamPotential__get_parameter_names()
