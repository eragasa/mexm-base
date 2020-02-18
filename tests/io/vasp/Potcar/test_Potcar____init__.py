import pytest
import os
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

# testing properties follows below
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

def test_Potcar__path__relative_path():
    path = 'POTCAR'

    obj = Potcar()
    obj.path = path
    assert os.path.isabs(obj.path)
    assert obj.path == os.path.abspath(path)

def test_Potcar__path__absolute_path():
    path = os.path.abspath('POTCAR')

    obj = Potcar()
    obj.path = os.path.abspath(path)
    assert obj.path == os.path.abspath(path)

def test_Potcar__path__bad_type():
    path = []
    obj = Potcar()
    with pytest.raises(TypeError):
        obj.path = []

def test_Potcar__encut_max__float():
    obj = Potcar()
    obj.encut_max = 100.
    assert isinstance(obj.encut_max, float)

def test_Potcar__encut_max__int():
    obj = Potcar()
    obj.encut_max = 100
    assert isinstance(obj.encut_max, float)

def test_Potcar__encut_max__castable_string():
    obj = Potcar()
    obj.encut_max = "100"
    assert isinstance(obj.encut_max, float)

def test_Potcar__encut_max__uncastable_string():
    obj = Potcar()
    with pytest.raises(ValueError):
        obj.encut_max = 'abc'

def test_Potcar__encut_min__float():
    obj = Potcar()
    obj.encut_min = 100.
    assert isinstance(obj.encut_min, float)

def test_Potcar__encut_min__int():
    obj = Potcar()
    obj.encut_min = 100
    assert isinstance(obj.encut_min, float)

def test_Potcar__encut_min__castable_string():
    obj = Potcar()
    obj.encut_min = "100"
    assert isinstance(obj.encut_min, float)

def test_Potcar__encut_min__uncastable_string():
    obj = Potcar()
    with pytest.raises(ValueError):
        obj.encut_min = 'abc'

def test_Potcar__symbols__list_of_strings():
    symbols = ['Si']
    obj = Potcar()
    obj.symbols = symbols
    assert isinstance(obj.symbols, list)
    assert obj.symbols == symbols

def test_Potcar__symbols__string():
    symbols = 'Si'

    obj = Potcar()
    obj.symbols = symbols
    assert isinstance(obj.symbols, list)
    assert obj.symbols == ['Si']
    