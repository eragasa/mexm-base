import pytest
import os
import shutil
from distutils import dir_util
from mexm.io.vasp import Oszicar

@pytest.fixture
def resourcedir(tmpdir, request):

    filename = request.module.__file__
    src_resource_dir = os.path.join(
        os.path.dirname(filename),
        'resource'
    )

    if os.path.isdir(src_resource_dir):
        tmpdir.mkdir('resource')
        dir_util.copy_tree(
            src_resource_dir, 
            os.path.join(str(tmpdir),'resource')
        )
    
    print(str(tmpdir))
    print(os.listdir(str(tmpdir)))
    assert os.path.isdir(os.path.join(str(tmpdir),'resource'))
    return tmpdir

@pytest.fixture
def oszicar_path(resourcedir):
    return os.path.join(resourcedir, 'resource', 'OSZICAR')

def test__read(oszicar_path):
    o = Oszicar()
    o.read(path=oszicar_path)

    assert isinstance(o.n_ionic, int)


def dev_Oszicar__read():
    oszicar_path = os.path.join('resource', 'OSZICAR')
    oszicar = Oszicar()
    assert oszicar.path is None
    assert oszicar.n_scf is None
    assert oszicar.scf_info is None
    assert oszicar.ionic_info is None
    oszicar.read(path=oszicar_path)
    for i_ionic, scf_info in enumerate(oszicar.scf_info):
        print('i_ionic:{}'.format(i_ionic))
        for i, v in enumerate(scf_info):
            print(i,v)

    for ionic_info in oszicar.ionic_info:
        print(ionic_info)
    print('n_ionic:{}'.format(oszicar.n_ionic))

if __name__ == "__main__":
    dev_Oszicar__read()