import pytest
from collections import OrderedDict
import numpy as np
from mexm.util import is_number
from mexm.structure import Atom

def test__init__():
    case = OrderedDict([
        ('symbol','Ni'),
        ('position',[0.,0.,0]),
        ('magmom',0),
        ('atom_id',None),
        ('exp_position', np.array([0.,0.,0.]))
    ])

    atom = Atom(symbol=case['symbol'],
                position=case['position'],
                magmom=case['magmom'],
                atom_id=case['atom_id'])

    assert isinstance(atom.symbol, str)
    assert isinstance(atom.position, np.ndarray)
    assert isinstance(atom.atom_id, str) or atom.atom_id is None

    assert atom.symbol == case['symbol']
    np.testing.assert_array_equal(atom.position, case['exp_position'])
    assert atom.magnetic_moment == case['magmom']
    assert atom.atom_id is None

initialization_args = [
    'symbol',
    'position',
    'magmom',
    'atom_id'
]

initialization_cases = OrderedDict()
initialization_cases['case1'] = OrderedDict([
    ('symbol','Ni'),
    ('position',[0.,0.,0]),
    ('magmom',0),
    ('atom_id',None),
    ('exp_position', np.array([0.,0.,0.]))
])

cases = ((case for case in initialization_cases.values()))
@pytest.mark.parametrize(
    'case',
    cases
)
def test__init__allcases(case):

    atom = Atom(symbol=case['symbol'],
                position=case['position'],
                magmom=case['magmom'],
                atom_id=case['atom_id'])

    assert isinstance(atom.symbol, str)
    assert isinstance(atom.position, np.ndarray)
    assert isinstance(atom.atom_id, str) or atom.atom_id is None

    assert atom.symbol == case['symbol']
    np.testing.assert_array_equal(atom.position, case['exp_position'])
    assert atom.magnetic_moment == case['magmom']
    assert atom.atom_id is None

if __name__ == "__main__":
    atom = Atom(symbol='Ni',position=[0.,0.,0.])
