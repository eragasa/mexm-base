# -*- coding: utf-8 -*-

"""Input and output functions and classes for VASP """
__author__ = "Eugene J. Ragasa"
__copyright__ = "Copyright (C) 2016,2017"
__license__ = "Simplified BSD License"
__version__ = "1.0"

import os, shutil, pathlib
import re
import copy
#import pyflamestk.base as base
import pypospack.crystal as crystal
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
    poscar.read(filename=filename)
    return poscar

def write_poscar_file(self,obj_poscar,filename='POSCAR'):
    obj_poscar.write(filename)

def read_incar_file(filename):
    incar = Incar()
    incar.read(filename=filename)
    return incar

def make_super_cell(obj, scp):
    sc = base.make_super_cell(copy.deepcopy(obj), list(scp))
    return copy.deepcopy(Poscar(sc))

from mexm.io.vasp.incar import Incar
from mexm.io.vasp.outcar import Outcar
from mexm.io.vasp.poscar import Poscar
from mexm.io.vasp.kpoints import Kpoints
from mexm.io.vasp.potcar import Potcar
# *****************************************************************************
# ****     CORE CLASSES                                                    ****
# *****************************************************************************

class VaspSimulation(object):
    """ class for managing vasp simulations

    This class encapsulates are variety of object for a vasp simulation

    Args:
        sim_dir(str): the path of this simulation
        xc(str): the exchange correlation functional

    Attribute:
        poscar (pypospack.io.poscar): class for mananging IO of structures for vasp.
        incar (pypospack.io.incar): class for managing IO of DFT configuration for vasp
        kpoints (pypospack.io.kpoints): defines the the grid for BZ zone integration.
        potcar (pypospack.io.potcar): defines potential file

    """
    def __init__(self,sim_dir,xc='GGA'):
        self.sim_dir = None

        self.is_req_met = False
        self.is_job_pending = True
        self.is_job_initalized = False
        self.is_job_submitted = False
        self.is_job_complete = False
        self.is_job_finished = False

        # vasp input/output filehandlers
        self.poscar = Poscar()
        self.incar = Incar()
        self.kpoints = Kpoints()
        self.potcar = Potcar()
        self.symbols = None

        # set simulation directory
        self.__check_restart_info(sim_dir)
        self.__set_simulation_directory(sim_dir)

    def __check_restart_info(sim_dir):
        if os.path.exists(self.sim_dir):
            pass

    def __set_simulation_directory(self,sim_dir):
        pass

    def read_incar(self,filename='INCAR'):
        self.incar.read(filename=filename)

    def write_incar(self,filename='INCAR'):
        self.incar.write(filename=filename)

    def read_poscar(self,filename='POSCAR'):
        self.poscar.read(filename)

    def write_poscar(self,filename='POSCAR'):
        self.poscar.write(filename)

    def write_kpoints(self,filename='KPOINTS'):
        self.kpoints.write(filename)

    def write_potcar(self,filename='POTCAR'):
        self.potcar.write(filename)

    def read_simulation_cell(self,filename='POSCAR'):
        self._poscar.read(filename)

    def __get_symbols_poscar(self):
        self.symbols = list(self.poscar.symbols)

class VaspMinimizeStructure(object):
    """ class for managing vasp structural minimizations """
    def __init__(self,sim_dir,structure, xc = 'GGA'):
        VaspSimulation.__init__(self)

        if instance(structure,str):
            self.__process_poscar_file(structure)

    def __process_poscar_file():
        pass
