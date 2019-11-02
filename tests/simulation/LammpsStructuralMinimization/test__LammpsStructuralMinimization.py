import pytest
import os
from mexm.simulation import LammpsStructuralMinimization

init_kwargs = {
    'name':'test_simulation_name',
    'simulation_path':'test_simulation_directory',
    'structure_path':os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'resources',
        'POSCAR'),
    'bulk_structure_name':None
}

def dev__LammpsStructuralMinimization____init__():
    o = LammpsStructuralMinimization(**init_kwargs)

def test__LammpsStructuralMinimization____init__():
    o = LammpsStructuralMinimization(**init_kwargs)

if __name__ == '__main__':
    o = LammpsStructuralMinimization(**init_kwargs)
