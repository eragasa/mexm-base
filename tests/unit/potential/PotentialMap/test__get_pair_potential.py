import pytest
from mexm.potential import PairPotential, pair_potential_names
from mexm.potential.loader import get_pair_potential

@pytest.mark.parametrize('name,symbols',[(k,['Ni']) for k in pair_potential_names])
def test__get_pair_potential(name,symbols):
    o = get_pair_potential(name,symbols)
    assert isinstance(o, PairPotential)
