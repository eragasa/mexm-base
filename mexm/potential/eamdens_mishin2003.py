__author__ = "Eugene J. Ragasa"
__copyright__ = "Copyright (C) 2017"
__license__ = "Simplified BSD License"
__version__ = 20171102

import copy
import numpy as np
from collections import OrderedDict
from pypospack.potential import EamDensityFunction

def func_cutoff_mishin2003(r,rc,hc):
    x = (r-rc)/hc

    if isinstance(r,np.ndarray):
        psi = np.ones(r.size) * (x**4)/(1+x**4)
        cutoff_ind = np.ones(r.size)
        cutoff_ind[r > rc] = 0
        return cutoff_ind*psi
    else:
        if r>rc:
            return 0
        else:
            return (x**4)/(1+x**4)
    
    # define the cutoff indicator, 1 except when x > x_cut
    cutoff_ind = np.ones(r.size)
    cutoff_ind[r > rc] = 0

def func_cutoff_mishin2003_r0(r, h0):
    x = r/h0

    if isinstance(r,np.ndarray):
        psi = np.ones(r.size) * (x**4)/(1+x**4)

def func_mishin2003_density(r,r0,A0,B0,C0,y,gamma):
    """
    Reference:
        Y. Mishin.  Acta Materialia. 52 (2004) 1451-1467
    """

    z = r - r0

    exp_gamma_z = np.exp(-gamma*z)
    density = A0*z**y*exp_gamma_z*(1+B0*exp_gamma_z)+C0

    return density

def func_mishin2003_density_w_cutoff(r,r0,A0,B0,C0,y,gamma,rc,h):

    rho = func_mishin2003_density(
            r=r,
            r0=r0,
            A0=A0,
            B0=B0,
            C0=C0,
            y=y,
            gamma=gamma)
    psi = func_cutoff_mishin2003(r=r,rc=rc,h=h)
    return psi*rho

class Mishin2003DensityFunction(EamDensityFunction):
    """
    Args:
        symbols(list of str)
    Attributes:
        symbols(list of str)
        potential_type(str): This is set to 'eamembed_universal'
        parameter_names(list of str)
        parameters(OrderedDict): The key is the symbol associated with the
            embedding function.  On initialization, the value of each parameter
            is set to None.
        density(OrderedDict): The key is the symbol associated with the
            embedding function.
        N_r(int)
        d_r(float)
        r_max(float)
        r(numpy.ndarray)
    """

    density_function_parameters = ['A0','B0','C0','y','gamma']
    def __init__(self,symbols):
        EamDensityFunction.__init__(
                self,
                symbols=symbols,
                potential_type='eamdens_mishin2003')
        self.density_function = function_mishin2003_density

    def _init_parameter_names(self):
        self.parameter_names = []
        for s in self.symbols:
            for p in self.density_function_parameters:
                pn = "{}_{}".format(s,p)
                self.parameter_names.append(pn)

    def _init_parameters(self):
        self.parameters = OrderedDict()
        for p in self.parameter_names:
            self.parameters[p] = None

    def evaluate(self,r,parameters,r_cut=None):
        """

        Given a vector of interatomic distances, r, passed in as variable
        r, and the associated parameters of the potential.  This method
        sets the density attribute.

        Args:
            r(numpy.ndarray): This should be named as rho because it
                represents the electron density being evaluated.
            parameters(OrderedDict): This is a dictionary of the parameters
                of the embedding function for each atom.  The key is a
                string containing the ISO chemical symbol of the element.
                The value should be a numeric value.
            r_cut(float): This would be the density cutoff.  However the
                embedding energy is increasing with increasing electron
                density so the a r_cut has no physical meaning.  Any
                variable passed into r_cut will be ignored.
        """
        assert isinstance(r,np.ndarray) or isinstance(r,float)
        assert isinstance(parameters,OrderedDict)
        assert type(r_cut) in [int,float,type(None)]
        # attribute.parameters[p] <--- arg:parameters[p]
        for s in self.symbols:
            for p in self.density_func_parameters:
                pn = "{}_{}".format(s,p)
                try:
                    self.parameters[pn] = parameters[pn]
                except KeyError as e:
                    print(80*'-')
                    print("{:^80}".format("DEBUGGING INFORMATION"))
                    print(80*'-')
                    print('pn:{}'.format(pn))
                    print('arg -> parameters:')
                    for k,v in parameters.items():
                        print("    {}:{}".format(k,v))
                    print('attr -> density_func_parameters')
                    for v in self.density_func_parameters:
                        print("    {}".format(v))
                    raise
        # cannot evaluate because
        for pn,pv in self.parameters.items():
            if pv is None:
                return False

        self.density_evaluations = OrderedDict()

        # each species has a unique density function
        for s in self.symbols:
            A0 = self.parameters['{}_A0'.format(s)]
            B0 = self.parameters['{}_B0'.format(s)]
            C0 = self.parameters['{}_C0'.format(s)]
            y = self.parameters['{}_y'.format(s)]
            gamma = self.parameters['{}_gamma'.format(s)]

            parameters = [A0,B0,C0,y,gamma]
            if r_cut is None:
                density = self.density_function(r,*parameters)
                self.density_evaluations[s] = copy.deepcopy(density)
            else:
                density = self.density_function(r,rho0,beta,r0)
                rcut = np.max(r[np.where(r<r_cut)])
                rcut_step = r[1] - r[0]
                density_rc = self.density_function(rcut,*parameters)
                density_rc_p1 = self.density_function(
                    rcut + rcut_step,
                    *parameters
                )
                density_rc_m1 = self.density_function(
                    rcut-rcut_step,
                    *parameters
                )
                drhodr_at_rc = (density_rc_p1 - density_rc)/rcut_step

                density = density - density_rc -drhodr_at_rc * (r-rcut)
                density[np.where(r>=_rcut)] = 0
                self.density_evaluations[s] = copy.deepcopy(_rho)

        return copy.deepcopy(self.density_evaluations)

if __name__ == '__main__':

    symbols = ['Ni']
    p = ExponentialDensityFunction(symbols=symbols)
    print(p.potential_type)
