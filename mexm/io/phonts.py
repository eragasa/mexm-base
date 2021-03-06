# -*- coding: utf-8 -*-
"""pypospack.io.phonts

This module provides input and output routines and classes for managing
simulations for Phonon Transport Simulation (PhonTS), written by 
A. Chernatiynskiy and S.R. Phillpot.  PhonTS is a lattice dynamics code 
that calculates thermal conductivity via the solution of the Boltzmann 
Transport Equation (BTE) for phonons.

This module's purpose is to automate the work required to interface PhonTS to
other codes such as LAMMPS for additional potentials, and first principals
electronic structure calculations (VASP).  While an interface is defined
for Quantum Expresso QE) for PhonTS, this interface is not implemented with
pypospack.io.phonts.

For a more a more in-depth understand of the PhonTS refer to the foundation
papers:

A. Chernatiynskiy and S.R. Phillpot, PRB 82, 134301 (2010)
A. Chernatiynskiy and S.R. Phillpot, Comp. Phys. Comm. (2015)

This module does not implement all the functionality which is available in
PhonTS.

Requirements
============

The use of this module requires setting the enviornment variable the 
.bash_profile or similar script on your system

export PHONTS_BIN=~/bin/PhonTS

Job Schedulers
==============

Due to the wide variety and implementations of the cluster job schedulers,
it is not possible to write all the possibilities of the job scheduler. The
general strategy for dealing with job submissions is to create a 

pypospack.io.slurm
pypospack.io.rocks
pypospack.io.pbs

"""
__author__ = "Eugene J. Ragasa, Xie Xiong"
__copyright__ = "Copyright (C) 2016,2017"
__license__ = "Simplified BSD License"
__version__ = "1.0"

import os, shutil, pathlib, copy, shlex, subprocess,sys
import numpy as np
from collections import OrderedDict
import pypospack.io.vasp as vasp
import pypospack.io.slurm as slurm
import pypospack.crystal as crystal
import pypospack.potential as potential
import pypospack.crystal as crystal
from pypospack.task import Task
from pypospack.crystal import get_amu
# *****************************************************************************
# ****    ERROR EXCEPTION HANDLING CLASSES                                 ****
# *****************************************************************************

class PhontsError(Exception):
    def __init__(self,*args,**kwargs):
        """Error class for reading/writing VASP INCAR IO issues """
        Exception.__init__(self,*args,**kwargs)

# *****************************************************************************
# ****     CORE CLASSES                                                    ****
# *****************************************************************************
PHONTS_INTERACTIONS = ['AbInitio']
PHONTS_FP_INTERFACES = ['VASP','QE','LAMMPS']
job_schedulers = ['slurm','rocks','pbs']


def simulation_cell_to_phonts_string(simulation_cell,charges=None):
    """

    This function converts as simulation cell and a dictionary of charges
    into the simulation cell secton of the PhonTS input file.

    Args:
        simulation_cell(pypospack.crystal.SimulationCell): This arguement
            expects the simulation cell to either to be a SimulationCell
            object, or an object which inherits those methods.
        charges(OrderedDict): This keys of this dictionary should have the 
            ISO chemical symbols of the atoms while the values of these 
            keys should provide floats of the charge.
    Returns:
        (str): a string of the the simulation cell in PhonTS format.
    """
    if not isinstance(simulation_cell,crystal.SimulationCell):
        err_msg = 'simulation cell is not an instance of '
        err_msg += 'pypospack.crystal.SimulationCell'
        raise ValueError(err_msg)

    _charges = OrderedDict()
    if charges is None:
        for s in simulation_cell.symbols:
            _charges[s] = 0.0
    else:
        for c in charges:
            _charges[c] = charges[c]

    str_out = "species {n_symbols}\n".format(
            n_symbols=len(simulation_cell.symbols))
    for s in simulation_cell.symbols:
        str_out += "{s} {amu} {chrg}\n".format(
                s=s,
                amu=get_amu(s),
                chrg=_charges[s])
    str_out += "Lattice {:10.6f}\n".format(1.0)
    str_out += "cell {a1:10.6f} {a2:10.6f} {a3:10.6f}\n".format(
        a1=simulation_cell.a1,
        a2=simulation_cell.a2,
        a3=simulation_cell.a3)
    str_out += "natoms {n}\n".format(n=simulation_cell.n_atoms)
    str_out += "fractional\n"
    for s in simulation_cell.symbols:
        for a in simulation_cell.atomic_basis:
            if a.symbol == s:
                str_out += "{s} {a1:10.6f} {a2:10.6f} {a3:10.6f}\n".format(
                        s=s,
                        a1=a.position[0],
                        a2=a.position[1],
                        a3=a.position[2])
    return str_out

def abinitio_interface_to_string(
        fp_interface='VASP',
        is_prep_step=True,
        numerical_2der=True, 
        numerical_3der=True,
        d3_cutoff=5.0,
        delta=0.005):
    """
    Args:
        fp_interface(str): first-principals interface.  Can be VASP, QE or
            LAMMPS.  Default is set to LAMMPS.
        numerical_2der(bool):
        numerical_3der(bool):
        d3_cutoff(float):
    """
    #<--- check the arguments of the functions
    if fp_interface not in ['VASP','QE','LAMMPS']:
        msg_out = "fp_interface must either be VASP, QE, or LAMMPS or None"
        raise ValueError(msg_out)
    if type(is_start) is not bool:
        raise ValueError("is_start must be a boolean")
    if type(numerical_2der) is not bool:
        raise ValueError("numerical_2der must be boolean")
    if type(numerical_3der) is not bool:
        raise ValueError("numerical_3der must be boolean")
    if type(asr_3der) is not bool:
        raise ValueError("asr_3der must be boolean")
    #if type(3d_cutoff) not in [int,float]:
    #    raise ValueError("3d_cutoff must be a numerical value")

    #<--- nested function to convert bool to 'T' or 'F'
    def bool2char(b):
        if b is True: 
            return 'T'
        else: 
            return 'F'

    str_out = \
        (
            "FP_interface {fp_interface}\n"
            "AbInitio {ab_init_0} {ab_init_1}\n"
            "numerical_2der {num_2der}\n"
            "numerical_3der {num_3der}\n"
            "delta {delta:10.6f}\n"
            "D3_cutoff {d3_cutoff:10.6f}\n"
        ).format(
            fp_interface=fp_interface,
            ab_init_0=bool2char(is_start),ab_init_1=bool2char(not is_start),
            numerical_2der=bool2char(numerical_2der),
            numerical_3der=bool2char(numerical_3der),
            delta=delta,
            d3_cutoff=d3_cutoff
        )
    return str_out

def phonts_kpoints_section_to_str(k1=9,k2=9,k3=9,kbte=1):
    """ Define the kpoint mesh for Phonons

    Defines the k-point mesh on which phonon properties are to be calculated.
    kx, ky, and kz determine resolutions in the reciprocal space.  PhonTS
    automatically create an odd-valued grid, even if an even-grid is provided.

    Args:
        kx(int): kpoint mesh resolution in the b1 direction, reciprocal lattice
        ky(int): kpoint mesh resolution in thee b2 direction, reciprocal lattice
        kz(int): kpoint mesh resolution in the b3 direction, reciprocal lattice
        kbte(int): additional resolution for the finer grid in the z direction,
            for more accurate determination of the energy conservation surface
            in thermal conductivity calculations.
    """
    str_out = "kpoints {} {} {} {}".format(k1,k2,k3,kbte)
    return str_out

def phonts_bte_section():
    pass

def phonts_dispersions():
    pass


# *****************************************************************************
# ****     CORE CLASSES                                                    ****
# *****************************************************************************
class PhontsInputFile(object):
    """
    Args:
        force_evaluation(str):
        phonon_kpoints(list of int): K-point mesh in on which phonon properties
            are to be calculated.  It should be an array with four elements,
            [N1,N2,N3,N4], where N4 specifies the finer grid along the z-axis
            for more accurate determination of the energy conversation surface
            in thermal conductivity simulations.

    """
    def __init__(self,
            filename='phonon_input.dat',
            structure_filename='POSCAR',
            phonts_configuration=None):

        # intitialize attributes    
        self._interaction_type = None

        # process constructor arguements
        self.filename = filename
        self.structure_filename = structure_filename
        if phonts_configuration is not None:
            self.phonts_configuration = copy.deepcopy(phonts_configuration)

    def write(self,filename=None):
        if filename is not None:
            self.filename = filename

        str_phonts_input = self.get_header_section()
        str_phonts_input += self.get_simulation_cell_section()
        str_phonts_input += self.get_iteraction_section()
        str_phonts_input += self.get_calculation_section()
        str_phonts_input += "\nend\n"

        with open(filename,'w') as f:
            f.write(str_phonts_input)


    def process_phonts_configuration(self,phonts_configuration=None):
        """
        Args:
            phonts_configuration(dict):
        """
        if phonts_configuration is not None:
            self.phonts_configuration = copy.deepcopy(phonts_configuration)

        #process interaction type
        self.interaction_type = self.phonts_configuration['interaction_type']
        if self.interaction_type == 'AbInitio':
            self.is_prep_step = self.phonts_configuration['is_prep_step']
            self.fp_interface = self.phonts_configuration['fp_interface']
            self.numerical_2der = self.phonts_configuration['numerical_2der']
            self.numerical_3der = self.phonts_configuration['numerical_3der']
            self.d3_cutoff = self.phonts_configuration['d3_cutoff']
            self.delta = self.phonts_configuration['delta']

        self.calculation_type = self.phonts_configurationp['calculation_type']
        if self.calculation_type == 'iterations':
            self.iter_steps = self.phonts_configuration['iter_steps']
            self.phonons_kpoints = self.phonts_configuration['phonon_kpoints']
            self.temperature = self.phonts_configurationp['temperature']

    def on_interaction_type_changed(self):
        if self.interaction_type == 'AbInitio':
            self.is_prep_step = True
            self.fp_interface = 'VASP'
            self.numerical_2der = True
            self.numerical_3der = True
            self.d3_cutoff = 5.0
            self.delta=0.005

    @property
    def interaction_type(self):
        return self._interaction_type

    @interaction_type.setter
    def interaction_type(self,interaction_type):
        if interaction_type not in PHONTS_INTERACTIONS:
            msg_err = (
                 "interaction_type is not supported. Supported interactions "
                 "types supported by pypospack is contained in "
                 "pypospack.io.phonts.PHONTS_INTERACTIONS.")
            raise ValueError(msg_err)
        self._interaction_type = interaction_type
        self.on_interaction_type_changed()

    def write(self,filename=None):
        if type(filename) is str:
            self.filename = filename

        str_phonts_input = ""
        str_phonts_input += self.get_header_section()
        str_phonts_input += self.get_simulation_cell_section()
        str_phonts_input += self.get_force_evaluation_section()
        str_phonts_input += self.get_phonts_calculated_properties()
        with open(self.filename,'w') as f:
            f.write(str_phonts_input)
    
    def get_header_section(self):
        str_out = "# PhonTS input file created pypospack.\n"

    def get_simulation_cell_section(self,structure_filename=None):
        if type(structure_filename) is str:
            self.structure_filename = structure_filename
        self.read_poscar_file()

        str_out += "# {:*^78}\n".format('simulation cell')
        charges = None
        if self.potential is not None:
            if self.potential.is_charge:
                charges = self.potential.get_charges()
        str_out += simulation_cell_to_phonts_string(
            simulation_cell=self.structure,
            charges=charges)
   
    def get_interaction_section(self):
        str_out = "# {:*^78}\n".format('INTERACTION SECTION')
        if self.interaction_type == 'AbInitio':
            str_out += abinitio_iterface_to_string(
                    fp_interface=self.fp_interface,
                    is_prep_step = self.is_prep_step,
                    numerical_2der= self.numerical_2der,
                    numerical_3der=self.numerical_3der,
                    d3_cutoff=self.d3_cutoff,
                    delta=self.delta)
    
    def get_calculation_section(self):
        def bool2char(b):
            if b:
                return 'T'
            else:
                return 'F'
        str_out = "# {:*^78}\n".format('INTERACTION SECTION')
        if self.calculation_type == 'iterations':
            str_out += (
                    "Iterations {is_iterations}\n"
                    "iter_steps {iter_steps}\n"
                    "kpoints {k1} {k2} {k2} {k4}\n"
            ).format(
                is_iterations=bool2char(True),
                iter_steps=self.phonts_configuration['iter_steps'],
                k1=self.phonts_configuration['phonon_kpoints'][0],
                k2=self.phonts_configuration['phonon_kpoints'][1],
                k3=self.phonts_configuration['phonon_kpoints'][2],
                k4=self.phonts_configuration['phonon_kpoints'][3]
            )
            temperature = self.phonts_configuration['temperature']
            if len(temperature) == 1:
                str_out += "temperature {t1}\n".format(
                        t1=temperature[0])
            elif len(temperature) == 3:
                str_out += "temperature {t1} {t2} {N_t}\n".format(
                    t1=temperature[0],
                    t2=temperature[1],
                    N_t=temperature[2])
            else:
                raise ValueError()
    def read_poscar_file(self,filename=None):
        if type(filename) is str:
            self.structure_filename = filename
        if self.structure_filename is None:
            raise ValueError('PhontsInputFile requires a structure file')

        self.simulation_cell = vasp.Poscar()
        self.simulation_cell.read(self.structure_filename)

class PhontsBteData(object):
    """
    Args:
        directory(str): the directory where the phonts simulation
            output files exist
        natoms(int):number of atoms in the simulation cel
    Attributes:
        directory(str): the directory where the phonts simulation
            output files exist
        ph_lt_file(pypospack.io.phonts.PhononLifetimeFile)
        ph_freq_file(pypospack.io.phonts.PhononFrequencyFile)
        natoms(int):number of atoms in the simulation cel
    """

    def __init__(self,directory,natoms):
        self.directory =directory
        self.ph_lt_file = None
        self.ph_freq_file = None

        self.ph_lt_filename = 'phon_lifetime.dat'
        self.ph_freq_filename = 'freq.dat'

        self.natoms = natoms
        self.data = None

    def read(self,directory=None):
        if directory is not None:
            self.directory = directory
            
        self.ph_lt_file = PhononLifetimeFile(
            natoms=self.natoms,
            filename=os.path.join(
                self.directory,
                self.ph_lt_filename))
        self.ph_freq_file = PhononFrequencyFile(
            natoms=self.natoms,
            filename=os.path.join(
                self.directory,
                self.ph_freq_filename))
        
        self.ph_lt_file.read()
        self.ph_freq_file.read()

    def build_data(self):
        self.data = OrderedDict()
        for temp in self.ph_lt_file.temp:
            print('temp={}'.format(temp))
            self.data[temp] = None
            self.build_data_at_temp(temp)


    def build_data_at_temp(self,temp):
        """
        This method consolidates the data contained in two different files
        so that we can compare phonon frequencies with with phonon lifetimes.
        
        Args:
            temp(int): the temperature from the BTE calculation, this value
                must be in list of values contained in the list ph_lt_file.temp
        """
        if self.data is None:
            self.data = OrderedDict()

        self.data[temp] = [] # initialize our list
        
        self.kpoint_keys_format = "{kp1:.6f}_{kp2:.6f}_{kp3:.6f}"

        freq_n_rows, freq_n_cols = self.ph_freq_file.data.shape
        lt_n_rows, lt_n_cols = self.ph_lt_file.data[temp].shape

        #these indices are the column index for the columns kp1,kp2,kp3 in 
        #phonon frequency file (ph_fr_file) 
        freq_kp1_idx = self.ph_freq_file.col_names.index('kp1')
        freq_kp2_idx = self.ph_freq_file.col_names.index('kp2')
        freq_kp3_idx = self.ph_freq_file.col_names.index('kp3')

        # these indices are the the column indices for the columns kp1,kp2,kp3
        # in the lifetime frequency file (ph_lt_file)
        lt_kp1_idx = self.ph_lt_file.col_names.index('kp1')
        lt_kp2_idx = self.ph_lt_file.col_names.index('kp2')
        lt_kp3_idx = self.ph_lt_file.col_names.index('kp3')

        for i in range(freq_n_rows):
           freq_kpoint_key = self.kpoint_keys_format.format(
               kp1 = self.ph_freq_file.data[i,freq_kp1_idx],
               kp2 = self.ph_freq_file.data[i,freq_kp2_idx],
               kp3 = self.ph_freq_file.data[i,freq_kp3_idx])
           for j in range(lt_n_rows):
               lt_kpoint_key = self.kpoint_keys_format.format(
                   kp1 = self.ph_lt_file\
                          .data[temp][j,lt_kp1_idx],
                   kp2 = self.ph_lt_file\
                          .data[temp][j,lt_kp2_idx],
                   kp3 = self.ph_lt_file\
                          .data[temp][j,lt_kp3_idx])

               if freq_kpoint_key == lt_kpoint_key:
                   for k in range(3*self.natoms):
                       # here we are building the row for the phonon frequency
                       # and the associated limetime with that phonon
                       # ph_id(int) - unique integer assigned to a phonon for
                       #        identification
                       # kp1,kp2,kp3 - the location of the kpoint associated with
                       #     phonon frequency represented in the basis of the 
                       #     reciprocal lattice
                       # fr - this is the frequency of the phonon in meV
                       # lt - this is the phonon lifetime in ps
                       ph_id = len(self.data[temp])
                       kp1 = self.ph_lt_file\
                           .data[temp][j,lt_kp1_idx]
                       kp2 = self.ph_lt_file\
                           .data[temp][j,lt_kp2_idx]
                       kp3 = self.ph_lt_file\
                           .data[temp][j,lt_kp3_idx]

                       # we need the index associated with the phonon freq
                       fr_idx = self.ph_freq_file.col_names.index(
                           "freq{}".format(k+1))

                       # wew need the index associated with the phonon lifetime
                       lt_idx = self.ph_lt_file.col_names.index(
                           "lt{}".format(k+1))
                       fr = self.ph_freq_file.data[i,fr_idx]
                       lt = self.ph_lt_file.data[temp][j,lt_idx]
                       self.data[temp].append([
                           ph_id,
                           kp1,kp2,kp3,
                           fr,lt])
        self.data[temp] = np.array(self.data[temp])

class PhononLifetimeFile(object):
    
    def __init__(self,natoms,filename='phon_lifetime.dat'):
       self.col_names = ['index','kp1','kp2','kp3']\
                + ['lt{}'.format(i+1) for i in range(3*natoms)]
       self.natoms = natoms
       self.filename = filename
       self.data = read_phon_lifetime(self.filename)
       self.temp = [k for k,v in self.data.items()]

    def read(self):
       self.data = read_phon_lifetime(self.filename)
    
    def print(self):
       for k,v in self.data.items():
           print(k,v.shape)

class PhononFrequencyFile(object):
    
    def __init__(self,natoms,filename='freq.dat'):
        self.col_names = ['index','kp1','kp2','kp3']\
                + ['freq{}'.format(i+1) for i in range(3*natoms)]
        self.filename = filename
        self.data = None
        self.natoms = natoms

    def read(self,filename=None):
        if filename is not None:
            self.filename = filename

        try:
            with open(self.filename,'r') as f:
                lines = f.readlines()
        except FileNotFoundErr as e:
            raise
  
        values_all = []
        for i,line in enumerate(lines):
            args = line.strip().split()
            values_all.append([float(arg) for arg in args])
   
        self.data = np.array(values_all)

    def print(self):
        print(self.data.shape)

def get_data_from_phonts_file(filename):
    #def process_first_line(line):
    #    args = line.strip().split()
    #    args = [arg.strip() for arg in args]
    #    args = args[1:]
    #    return args
    
    #labels = None
    data = None
    data_all = None
    with open(filename) as f:
        lines = f.readlines()
    # except FileNotFoundErr
  
    #initialize variables
    values_all = []
    for i,line in enumerate(lines):
       # if i == 0:
           # labels = process_first_line(line)
       # else:
           args = line.strip().split()
           values_all.append([float(arg) for arg in args])
   
    data_all = np.array(values_all)
    
    return data_all

def get_freq_data(filename='freq.dat'):
    freq_data = get_data_from_phonts_file(filename)
    return freq_data


def read_phon_lifetime(filename='phon_lifetime.dat'):
    """
    Reads phonon lifetime information
    
    """

    def subselect_table_block(i_start,lines):
        i=i_start+1
        
        table = []
        while(lines[i].strip() !=""):
            args = lines[i].split()
            args = [arg.strip() for arg in args]
            args = [float(arg) for arg in args]
            table.append(args)
            i += 1
        return np.array(table)
    
    line = None #initialize
    with open(filename,'r') as f:
        lines = f.readlines()
    lines = [s.strip() for s in lines]
    
    temperatures = []
    phon_lifetime = OrderedDict()

    for il,line in enumerate(lines):
        if line.startswith('# Temp:'):
            args = line.split(':')
            T = int(float(args[1].strip()))
            temperatures.append(T)
            phon_lifetime[T] = subselect_table_block(il,lines)

    return {k:v.copy() for k,v in phon_lifetime.items()}

#******************************************************************************
# POST PROCESSING SCRIPTS
#******************************************************************************

class PhontsPdosDatafile(object):

    def __init__(self,filename=None):
        self.filename = filename
        self.data = None
        self.labels = None
        if filename is not None:
            self.read()

    @property
    def df(self):
        """(pandas.DataFrame)"""
        return self._df

    def read(self,filename='pdos.dat'):
        if filename is not None:
            self.filename = filename

        self.data,self.labels = get_pdos_data(self.filename)

def get_pdos_data(filename='pdos.dat'):
    
    def process_first_line(line):
        args = line.strip().split()
        args = [arg.strip() for arg in args]
        args = args[1:]
        return args

    pdos_labels = None
    pdos_data = None
    with open(filename,'r') as f:
        lines = f.readlines()
    # except FileNotFoundError

    #initialize variables
    values = []
    for i,line in enumerate(lines):
        if i == 0:
            pdos_labels = process_first_line(line)
        else:
            args = line.strip().split()
            values.append([float(arg) for arg in args])

    pdos_data = np.array(values)

    return pdos_data,pdos_labels
