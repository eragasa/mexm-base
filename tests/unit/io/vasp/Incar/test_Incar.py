import pytest
import os
from mexm.io.vasp import Incar

parent_path = os.path.parent_path(os.path.abspath(__file__))

@pytest.fixture
def incar_path():
    path = os.path.join(parent_path, 'INCAR')
    return path

@pytest.fixture
def incar_obj(incar_path):
    o = Incar()
    o.read(path=incar_path)
    return o

def test_Incar____init__():
    o = Incar()

def test_Incar__read(incar_path):
    o = Incar()
    o.read(path=incar_path)

def test_Incar__system_information_to_string_():
    o = Incar()
    o.system = 'test string'
    s = o.system_information_to_string_()
    assert isinstance(s, str)
    assert s == 'SYSTEM = {}\n\n'.format(o.system)

def test_Incar__set_tag_value():
    tag_name = 'ISTART'
    tag_value = 0
    o = Incar()
    o.set_tag_value(tag_name=tag_name, tag_value=tag_value)

def dev_Incar__set_tag_value__ISTART():
    tag_name = 'ISTART'
    tag_value = 0
    o = Incar()
    o.set_tag_value(tag_name=tag_name, tag_value=tag_value)

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

def dev_Incar__dos_information_to_string_():
    o = Incar()

    s = o.dos_information_to_string_()
    print(s)

if __name__ == "__main__":
    dev_Incar__set_tag_value__ISTART()
    dev_Incar__system_information_to_string_()
    dev_Incar__start_information_to_string_()
    dev_Incar__dos_information_to_string_()