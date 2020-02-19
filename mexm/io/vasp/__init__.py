# -*- coding: utf-8 -*-
import os, shutil, pathlib
import re
import copy
#import pyflamestk.base as base
#import pypospack.crystal as crystal
import numpy as np

# *****************************************************************************
# ****    ERROR EXCEPTION HANDLING CLASSES                                 ****
# *****************************************************************************
from mexm.io.vasp.incar import VaspIncarError
from mexm.io.vasp.poscar import VaspPoscarError
from mexm.io.vasp.potcar import VaspPotcarError

# *****************************************************************************
# ****    SOME CONVENIENCE FUNCTIONS                                       ****
# *****************************************************************************

def read_poscar_file(filename):
    poscar = Poscar()
    poscar.read(path=filename)
    return poscar

def write_poscar_file(self,obj_poscar,filename='POSCAR'):
    obj_poscar.write(filename)

def read_incar_file(filename):
    incar = Incar()
    incar.read(path=filename)
    return incar

def make_super_cell(obj, scp):
    sc = base.make_super_cell(copy.deepcopy(obj), list(scp))
    return copy.deepcopy(Poscar(sc))

# input files
from mexm.io.vasp.incar import Incar
from mexm.io.vasp.poscar import Poscar
from mexm.io.vasp.kpoints import Kpoints
from mexm.io.vasp.potcar import Potcar

# output files
from mexm.io.vasp.contcar import Contcar
from mexm.io.vasp.outcar import Outcar
from mexm.io.vasp.oszicar import Oszicar
class Chgcar(): pass

