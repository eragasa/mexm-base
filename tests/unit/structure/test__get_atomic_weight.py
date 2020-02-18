from mexm.structure import get_atomic_weight

def dev__get_atomic_weight():
    symbol = 'Mg'
    amu = get_atomic_weight(symbol=symbol)
    print('{} amu: {}'.format(symbol,amu))

def test__get_atomic_weight():
    symbol = 'Mg'
    amu = get_atomic_weight(symbol=symbol)
    assert isinstance(amu, float)


if __name__ == "__main__":
    dev__get_atomic_weight()
