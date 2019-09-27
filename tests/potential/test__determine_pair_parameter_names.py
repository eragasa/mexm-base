import pytest
from collections import OrderedDict

from mexm.potential import determine_pair_parameter_names

cases = OrderedDict()
cases['1sym_list'] = OrderedDict([
    ('symbols', ['Ni']),
    ('pair_parameter_names',  ['A','B','C']),
    ('expected_parameter_names', ['NiNi_A',
                                  'NiNi_B',
                                  'NiNi_C'])
])
cases['2sym_list'] = OrderedDict([
    ('symbols', ['Ni','Al']),
    ('pair_parameter_names', ['A','B','C']),
    ('expected_parameter_names', ['NiNi_A', 'NiNi_B', 'NiNi_C',
                                  'NiAl_A', 'NiAl_B', 'NiAl_C',
                                  'AlAl_A', 'AlAl_B', 'AlAl_C'] )
])

@pytest.mark.parametrize(
    "symbols,pair_parameter_names,expected_parameter_names",
    [tuple(v for v in case.values()) for case in cases.values()]
)
def test__determine_pair_parameter_names(
        symbols,
        pair_parameter_names,
        expected_parameter_names):

    parameter_names = determine_pair_parameter_names(symbols,
                                                     pair_parameter_names)
    assert parameter_names == expected_parameter_names

if __name__ == "__main__":
    pass
