# -*- coding: utf-8 -*-
"""This module contains classes to interact with GULP."""
__author__ = "Eugene J. Ragasa"
__copyright__ = "Copyright (C) 2017,2018,2019"
__license__ = "Simplified BSD License"
__version__ = "1.0"

from collections import OrderedDict
from mexm.exceptions import BadParameterException

from mexm.elements import ELEMENTS
from mexm.potential import MEXM_CHARGE_FORMAT
from mexm.potential import MEXM_PAIR_FORMAT

class Potential(object):
    """base class for potential

    Args:
        symbols(list of str): a list of symbols to use for the potential
        potential_type(str): a description for the type of potential this is
        is_charge(bool): if set to true, this potential is a charge potential, default: False
    """

    def __init__(self,
                 symbols,
                 potential_type=None,
                 is_charge=False):

        # define formatting strings

        # self.potential = None
        self.symbols = symbols
        self.potential_type = potential_type
        self.is_charge = is_charge

        # these attributes will be initialized by _init_parameter_names
        self.symbol_pairs = None
        self.parameter_names = None
        self._init_parameter_names()

        # these attributes will be initialized by _init_parameter_names
        self.parameters = None
        self._init_parameters()

    def _init_parameter_names(self):
        raise NotImplementedError

    def _init_parameters(self):
        raise NotImplementedError

    def evaluate(self, r, parameters, r_cut=False):
        """evaluate the potential

        Args:
            r(numpy.ndarray): a numpy array of interatomic distances
            parameters(OrderedDict): an dictionary of parameter values and keys
            r_cut(float,optional): the global cutoff for the potential
        """
        raise NotImplementedError

    def write_lammps_potential_file(self):
        """writes the lammps_potential file

        This method exists to write the lammps potential file to disk.  This
        method needs to be overriden to be implemented, in classes that
        inherit from this class.
        """

        raise NotImplementedError

    def lammps_potential_section_to_string(self):
        """generates the lammps string for the lammps potential sections

        Returns:
            str: the string value for the LAMMPS potential section that goes into the potential.mod file.
        """

        raise NotImplementedError


    def write_gulp_potential_section(self):
        """writes the gulp potential for a GULP string"""
        raise NotImplementedError

    def gulp_potential_section_to_string(self):
        """generates the potential section for a GULP string"""
        raise NotImplementedError

    def _get_mass(self, symbol):
        return ELEMENTS[symbol].mass

    def _get_name(self, symbol):
        return ELEMENTS[symbol].name.lower()

if __name__ == "__main__":
    o = Potential(symbols=['Ni'])
