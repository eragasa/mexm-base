__author__ = "Eugene J. Ragasa"
__copyright__ = "Copyright (C) 2018"
__license__ = "Simplified BSD License"
__version__ = 20180301

import copy
import numpy as np
from collections import OrderedDict
from mexm.potential import PairPotential
from mexm.potential import get_symbol_pairs
from mexm.potential import MEXM_2BODY_FMT, MEXM_HYBRID_2BODY_FMT

def func_bornmayer(r,phi0,gamma,r0):
    return phi0*np.exp(-gamma*(r-r0))


class BornMayerPotential(PairPotential):
    potential_type = 'bornmayer'
    is_base_potential = False
    parameter_names_global = []
    parameter_names_1body = []
    parameter_names_2body = ['phi0','gamma','r0','rcut']
    """ Implementation of a Born-Mayer repulsive potential

    Args:
        symbols(list of str)
    Attributes:
        symbols(list of str)

    """
    def __init__(self,symbols):
        PairPotential.__init__(self,
                symbols,
                is_charge=False)

    @staticmethod
    def function(r, phi0, gamma, r0, rcut):
        return phi0*np.exp(-gamma*(r-r0))


    def evaluate(self,r,parameters,r_cut=None):
        # <----------------------------check arguments are correct
        # assert isinstance(r,np.ndarray)
        assert isinstance(parameters,OrderedDict)
        assert type(r_cut) in [int,float,type(None)]

        # <----------------------------copy a local of the parameters
        for k in self.parameters:
            self.parameters[k] = parameters[k]

        # <----------------------------evaluate the parameters now
        self.potential_evaluations = OrderedDict()
        for s in self.symbol_pairs:
            # <------------------------extract the parameters for symbol pair
            phi0 = self.parameters['{}{}_phi0'.format(s[0],s[1])]
            gamma  = self.parameters['{}{}_gamma'.format(s[0],s[1])]
            r0 = self.parameters['{}{}_r0'.format(s[0],s[1])]
            # <------------------------embedded morse function

            _pair_name = '{}{}'.format(s[0],s[1])
            if r_cut is None:
                _V = func_bornmayer(r,phi0,gamma,r0)
                self.potential_evaluations[_pair_name] = copy.deepcopy(_V)
            else:
                _rcut = np.max(r[np.where(r < r_cut)])
                _h = r[1] - r[0]
                _V_rc = func_bornmayer(_rcut,phi0,gamma,r0)
                _V_rc_p1 = func_bornmayer(_rcut+_h,phi0,gamma,r0)
                _V_rc_m1 = func_bornmayer(_rcut-_h,phi0,gamma,r0)
                _dVdr_at_rc = (_V_rc_p1-_V_rc)/_h

                # <----- calculate morse with cutoff
                _V = func_bornmayer(r,phi0,gamma,r0)
                # <----- apply the cutoff
                _V= _V - _V_rc - _dVdr_at_rc * (r-_rcut)
                # <----- V=0, where r <= _rcut
                _V[np.where(r>=_rcut)] = 0.0

                self.potential_evaluations[_pair_name] = copy.deepcopy(_V)

        return copy.deepcopy(self.potential_evaluations)

    # same as parent class
    def lammps_potential_section_to_string(self):
        """string of the potential section in the lammps file"""
        raise NotImplementedError

    # same as parent class
    def gulp_potential_section_to_string(self):
        """string of the potential section in the gulp file"""
        raise NotImplementedError

    # same as parent class
    def phonts_potential_section_to_string(self):
        """string of the potential section in the phonts file"""
        raise NotImplementedError

    # same as parent class
    def write_lammps_potential_file(self):
        """write the lammps potential file to potential.mod"""
        raise NotImplementedError

    # same as parent class
    def write_gulp_potential_section(self):
        """write the potential section"""
        raise NotImplementedError

    def references(self):
        reference_dict = {}
        reference_dict['LammpsMorse'] \
                = "http://lammps.sandia.gov/doc/pair_morse.html"
        return reference_dict
