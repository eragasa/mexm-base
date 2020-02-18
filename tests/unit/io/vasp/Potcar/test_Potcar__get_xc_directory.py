import pytest
import os
from mexm.io.vasp import Potcar

def test_Potcar__get_xc_directory__gga():
    gga_path = os.environ['VASP_GGA_DIR']
    assert gga_path == Potcar.get_xc_directory(xc_type='gga')

def test_Potcar__get_xc_directory__lda():
    lda_path = os.environ['VASP_LDA_DIR']
    assert lda_path == Potcar.get_xc_directory(xc_type='lda')