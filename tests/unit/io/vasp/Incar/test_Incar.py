import pytest
from mexm.io.vasp import Incar

def test_Incar____init__():
    o = Incar()

def test_Incar__read():
    incar_path = 'INCAR'
    o = Incar()
    o.read(path=incar_path)

def test_Incar__system_information_to_string_():
    o = Incar()
    o.system = 'test string'
    s = o.system_information_to_string_()
    assert isinstance(s, str)
    assert s == 'SYSTEM = {}\n\n'.format(o.system)

def dev_Incar__system_information_to_string_():
    incar_path = 'INCAR'
    o = Incar()
    o.read(path=incar_path)
    s = o.system_information_to_string_()
    print(s)

def dev_Incar__start_information_to_string_():
    incar_path = 'INCAR'
    o = Incar()
    o.read(path=incar_path)

    s =o.start_information_to_string_()
    print(s)

if __name__ == "__main__":
    dev_Incar__system_information_to_string_()
    dev_Incar__start_information_to_string_()