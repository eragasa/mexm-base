import pytest

from mexm.io.vasp import Potcar
from mexm.io.vasp.potcar import VaspPotcarError

def test_Potcar____init__():
    obj = Potcar()
    assert obj.symbols == None
    assert obj.path == None
    assert obj.xc_type == 'gga'
    assert obj.encut_min_ == None
    assert obj.encut_max_ == None
    assert obj.models == None
    
def test_Potcar__xc_type__gga():
    obj = Potcar()
    obj.xc_type = 'gga'
    assert obj.xc_type == 'gga'
    obj.xc_type = 'GGA'
    assert obj.xc_type == 'gga'

def test_Potcar__xc_type__lda():
    obj = Potcar()
    obj.xc_type = 'lda'
    assert obj.xc_type == 'lda'
    obj.xc_type = 'LDA'
    assert obj.xc_type == 'lda'

def test_Potcar__xc_type__bad_xc_string():
    obj = Potcar()
    with pytest.raises(VaspPotcarError):
        obj.xc_type = 'bad'

def test_Potcar__xc_type__bad_type():
    obj = Potcar()
    with pytest.raises(TypeError):
        obj.xc_type = []