import pytest
from mexm.elements import ELEMENTS as elements
from mexm.elements import get_atomic_mass

def test__get_atomic_mass():
    symbol = 'C'
    assert get_atomic_mass(symbol) == elements[symbol].mass
