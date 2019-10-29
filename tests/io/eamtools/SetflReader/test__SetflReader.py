import os
from mexm.io.eamtools import SetflReader

resource_setfl_path = os.path.join(
    os.path.dirname(__file__),
    'Mishin-Ni-Al-2009.eam.alloy'
)

def test____init____no_path():
    o = SetflReader()
    assert isinstance(o.comments, list)
    assert len(o.comments, 0)
    assert o.comments is None
    assert isinstance(o.symbols, list)
    assert len(o.symbols, 0)
    assert isinstance(o.symbol_pairs, list)
    assert len(o.symbols_pairs, 0)
    assert o.N_rho is None
    assert o.d_rho is None
    assert o.N_r is None
    assert o.d_r is None
    assert o.r_cutoff is None

    assert isinstance(o.lattice_info, dict)
    assert isinstance(o.embedding_functions, dict)
    assert isinstance(o.density_functions, dict)
    assert isinstance(p.pair_functions, dict)


def dev__SetflReader():
    setfl = SetflReader()
    setfl.read(path=resource_setfl_path)
    print(setfl.comments)
    print(setfl.N_symbols)
    print(setfl.symbols)
    print(setfl.symbol_pairs)

    print(setfl.N_r*setfl.d_r)
    print(setfl.r_cutoff)
if __name__ == "__main__":
    dev__SetflReader()
