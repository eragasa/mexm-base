import pytest

from oszicar import Oszicar

def dev_Oszicar__read():
    oszicar_path = 'OSZICAR'
    o = Oszicar()
    o.read(path=oszicar_path)
    
if __name__ == "__main__":
    dev_Oszicar__read()