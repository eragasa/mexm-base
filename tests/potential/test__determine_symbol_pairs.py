import pytest
from collections import OrderedDict

from mexm.potential import determine_symbol_pairs

cases = OrderedDict()
cases['1sym_str'] = OrderedDict([
    ('symbols','Ni'),
    ('expected_pairs',[['Ni','Ni']])
])
cases['1sym_list'] = OrderedDict([
    ('symbols', ['Ni']),
    ('expected_pairs',[['Ni','Ni']])
])
cases['2sym_list'] = OrderedDict([
    ('symbols', ['Ni','Al']),
    ('expected_pairs',[ ['Ni', 'Ni'],
                        ['Ni', 'Al'],
                        ['Al', 'Al'] ])
])
cases['3sym_list'] = OrderedDict([
    ('symbols', ['Fe', 'Ni', 'Cr']),
    ('expected_pairs',[['Fe', 'Fe'],
                       ['Fe', 'Ni'],
                       ['Fe', 'Cr'],
                       ['Ni', 'Ni'],
                       ['Ni', 'Cr'],
                       ['Cr', 'Cr'] ])
])


@pytest.mark.parametrize(
    "symbols,expected_pairs",
    [tuple(v for v in case.values()) for case in cases.values()]
)
def test__determine_symbol_pairs(symbols, expected_pairs):
    assert expected_pairs == determine_symbol_pairs(symbols)

if __name__ == "__main__":
    pass
