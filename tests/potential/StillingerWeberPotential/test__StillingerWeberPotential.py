import pytest
from collections import OrderedDict
from mexm.potential import MEXM_3BODY_FMT
from mexm.potential import StillingerWeberPotential

@pytest.mark.parametrize(
    "symbols",
    [['Si']]
)
def test____init__noargs(symbols):
    potential = StillingerWeberPotential(symbols=symbols)
    assert isinstance(potential.parameter_names, list)
    assert isinstance(potential.parameters, OrderedDict)

if __name__ == "__main__":
    symbols = ['Si']
    potential = StillingerWeberPotential(symbols=symbols)
    print(type(potential))
    print(potential.potential_type)


    print(80*'-')
    print('{}.{}'.format(potential.potential_type,
                         'parameter_names')
    )
    print(80*'-')
    for k in potential.parameter_names:
        print(k)

    print(80*'-')
    print('{}.{}'.format(potential.potential_type,
                         'parameter_names')
    )
    print(80*'-')
    for k in potential.parameter_names:
        print(k)
