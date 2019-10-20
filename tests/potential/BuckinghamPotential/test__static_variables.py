import pytest
from collections import OrderedDict
from mexm.potential import BuckinghamPotential

def test__static_variables():
    assert isinstance(BuckinghamPotential.parameter_names_global, list)
    assert isinstance(BuckinghamPotential.parameter_names_1body, list)
    assert isinstance(BuckinghamPotential.parameter_names_1body, list)
    assert isinstance(BuckinghamPotential.potential_type, str)
    assert isinstance(BuckinghamPotential.is_charge, bool)

    assert BuckinghamPotential.parameter_names_global == ['cutoff']
    assert BuckinghamPotential.parameter_names_1body == ['chrg', 'cutoff']
    assert BuckinghamPotential.parameter_names_2body == ['A', 'rho', 'C', 'cutoff']
    assert BuckinghamPotential.potential_type == 'buckingham'
    assert BuckinghamPotential.is_charge

    if BuckinghamPotential.is_charge:
        'chrg' in BuckinghamPotential.parameter_names_1body
