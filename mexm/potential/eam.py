from collections import OrderedDict
import copy
import numpy as np
from mexm.potential import Potential
from mexm.potential import PairPotential
from mexm.potential import EamDensityFunction
from mexm.potential import EamEmbeddingFunction
from mexm.io.eamtools import SetflFile

from mexm.exception import MexmException
class MexmPotentialError(Exception): pass

class EamPotential(Potential):
    potential_type = 'eam'
    is_base_potential = False
    is_charge = False

    MEXM_EAM_PAIR_FORMAT = "pair_{symbol1}{symbol2}_{parameter_name}"
    MEXM_EAM_DENS_FORMAT = "dens_{symbol}{parameter_name}"
    MEXM_EAM_EMBED_FORMAT = "embed_{symbol}_{parameter_name}"
    """embedded energy method potential
    This class is for the modelling of an EAM potential
    Args:
       symbols(list of str):
       func_pairpotential(str):
       func_density(str):
       func_embedding(str):
       filename(str):

    Attributes:
       symbols(list of str): the list of symbols
       obj_pair(OrderedDict of PairPotential)
       obj_density(OrderedDict of EamDensityFunction)
       obj_embedding(OrderedDict of EamEmbeddingFunction)
       N_r(int): number of radial points, the distance between two atoms
       r_max(float): the maximum distance between two atoms
       r_cut(float): the cutoff distance between two atoms
       N_rho(int): the number of points in the electron density evaluation
       rho_max(float): the maximum electron density
    """
    def __init__(self,
            symbols,
            func_pair=None,
            func_density=None,
            func_embedding=None,
            filename=None):

        # these are pypospack.potential.Potential objects
        self.obj_pair = None
        self.obj_density = None
        self.obj_embedding = None

        self.N_r = None
        self.r_max = None
        self.r_cut = None

        self.N_rho = None
        self.rho_max = None

        # these will be numpy arrays
        self.r = None
        self.rho = None
        self.pair = None
        self.density = None
        self.embedding = None

        self.symbols = symbols

        self.setfl_filename_src = filename
        self.setfl_filename_dst = "{symbols}.eam.alloy".format(
                symbols="".join(self.symbols))
        self.setfl = None

        if func_pair is not None:
            self.set_obj_pair(func_pair=func_pair)
        if func_density is not None:
            self.get_obj_density(func_density=func_density)
        if func_embedding is not None: self.get_obj_embedding(fun_embedding=func_embedding)

        Potential.__init__(self,
                symbols=symbols,
                potential_type='eam',
                is_charge = False)

    @classmethod
    def get_parameter_names(cls,
                            symbols,
                            pair_type,
                            density_type,
                            embedding_type):
        from mexm.manager import PotentialManager

        parameter_names = []
        potential_types = [k.potential_type for k in PotentialManager.get_potential_types()]
        for potential in PotentialManager.get_potential_types():
            if potential.potential_type == pair_type:
                parameter_names = [
                    'pair_{}'.format(k)
                    for k in potential.get_parameter_names(symbols)
                ]

        print(PotentialManager.get_potential_types())

    def lammps_potential_section_to_string(self,setfl_dst_filename):
        """provide string for the potential section
        Args:
            setfl_dst_filename(str):the path that LAMMPS should read for the SETFL file
        Returns:
            str: the string of the lammps potential section
        """

        # set masses
        str_out = ''
        for i,s in enumerate(self.symbols):
            str_out += "mass {} {}\n".format(i+1,self._get_mass(s))
        str_out += "\n"

        # set groups
        for i,s in enumerate(self.symbols):
            str_out += "group {} type {}\n".format(s,i+1)
        str_out += "\n"

        str_out += "pair_style eam/alloy\n"
        str_out += "pair_coeff * * {setfl_dst_filename} {str_symbols}\n".format(
                    setfl_dst_filename=setfl_dst_filename,
                    str_symbols=" ".join(self.symbols))

        return str_out


    def _initialize_parameter_names(self):
        p_params = ['p_{}'.format(p) for p in self.obj_pair.parameter_names]
        d_params = ['d_{}'.format(p) for p in self.obj_density.parameter_names]
        e_params = ['e_{}'.format(p) for p in self.obj_embedding.parameter_names]
        self.parameter_names = list(p_params + d_params + e_params)

    def _init_parameters(self):
        if self.parameter_names is None:
            return

        self.parameters = OrderedDict()
        for p in self.parameter_names:
            self.parameters[p] = None

    def determine_r_max(self,a0,latt_type):
        _a0 = a0

        if latt_type == 'fcc':
            _d_1NN = 0.707 * _a0
            _d_2NN = 1.000 * _a0
            _d_3NN = 1.225 * _a0
            _d_4NN = 1.414 * _a0
            _d_5NN = 1.581 * _a0

        # r_max should be between the 3NN and 4NN
        _rcut = 0.5 * (_d_3NN + _d_4NN)
        return _rcut

    def determine_rho_max(self,a0,latt_type):
        _a0 = a0

        #extract parameters for the density function
        _parameters = OrderedDict()
        for k,v in self.parameters.items():
            if k.startswith('d_'):
                _parameter_name = k[2:]
                _parameters[_parameter_name] = v

        if latt_type == 'fcc':
            _d_1NN = 0.707 * _a0
            _d_2NN = 1.000 * _a0
            _d_3NN = 1.225 * _a0
            _d_O = 0.866 * _a0
            _d_T = 0.433 * _a0

            _natoms_1NN = 12
            _natoms_2NN = 6
            _natoms_O = 4
            _natoms_T = 2

        for s in self.symbols:
            _rhomax = _natoms_1NN * self.obj_density.evaluate(_d_1NN,_parameters)[s]
            _rhomax += _natoms_2NN * self.obj_density.evaluate(_d_2NN,_parameters)[s]
            _rhomax += _natoms_O * self.obj_density.evaluate(_d_O,_parameters)[s]
            _rhomax += _natoms_T * self.obj_density.evaluate(_d_T,_parameters)[s]

        _rhomax = float(_rhomax)
        return _rhomax

    def write_setfl_file(self,filename,symbols,
            Nr,rmax,rcut,
            Nrho,rhomax,
            parameters):
        assert type(filename) is str
        assert type(Nr) is int
        assert type(rmax) in [int,float]
        assert type(rcut) in [int,float]
        assert type(Nrho) is int
        assert type(rhomax) in [int,float]

        r = rmax * np.linspace(1,Nr,Nr)/Nr
        rho = rhomax * np.linspace(1,Nrho,Nrho)/Nrho

        self.evaluate(
                r=r,
                rho=rho,
                rcut=rcut,
                parameters=parameters)

        setfl_file = EamSetflFile()
        setfl_file.write(
                filename=filename,
                symbols=symbols,
                r=self.r,
                rho=self.rho,
                rcut=self.r_cut,
                pair=self.pair,
                density=self.density,
                embedding=self.embedding)

    def evaluate(self,r,rho,rcut,parameters):
        assert isinstance(r,np.ndarray)
        assert isinstance(rho,np.ndarray)
        assert type(rcut) in [float,int,type(None)]
        assert type(parameters) in [OrderedDict,dict]

        for p in self.parameters:
            self.parameters[p] = parameters[p]

        self.rcut = rcut
        self.r = copy.deepcopy(r)
        self.rho = copy.deepcopy(rho)
        self.evaluate_pair(r=r,rcut=rcut)
        self.evaluate_density(r=r,rcut=rcut)
        self.evaluate_embedding(rho=rho, rhocut=rcut)

    def _log(self,msg):
        print(msg)

    def set_obj_pair(self,func_pair):

        assert isinstance(func_pair,str)
        self.obj_pair = PotentialManager.get_Potential_by_name(
                func_pair,
                self.symbols
        )
        assert isinstance(self.obj_pair, PairPotential)

    def set_obj_density(self,func_density):

        assert isinstance(func_density,str)
        self.obj_density = PotentialManager.get_potential_by_name(
                func_density,
                self.symbols
        )

    def set_obj_embedding(self,func_embedding):

        assert isinstance(func_embedding,str)
        self.obj_embedding = PotentialManager.get_potential_by_name(
                func_embedding,
                self.symbols
        )

    def evaluate_pair(self,r,parameters=None,rcut=None):
        assert isinstance(r,np.ndarray)

        if parameters is not None:
            for p in self.parameters:
                self.parameters[p] = parameters[p]

        # pair potential parameters are prepended with 'p_'
        p_params = [p for p in self.parameters if p.startswith('p_')]

        # subselect the parameters required for the pair potential
        _parameters = OrderedDict()
        for p in p_params:
            _parameter_name = p.partition('_')[2]
            _parameters[_parameter_name] = self.parameters[p]

        self.obj_pair.evaluate(
                r=r,
                parameters=_parameters,
                r_cut=rcut)

        self.pair = copy.deepcopy(self.obj_pair.potential_evaluations)

    def evaluate_density(self,
            r,
            rcut=None,
            parameters=None):
        assert isinstance(r,np.ndarray) or isinstance(r,float)
        assert isinstance(rcut,float) or rcut is None
        assert isinstance(parameters,dict) or parameters is None

        #<--- check arguments of the function
        if parameters is not None:
            for p in self.parameters:
                self.parameters[p] = parameters[p]

        #<--- grab the parameters of the density function
        d_params = [p for p in self.parameters if p.startswith('d_')]

        _parameters = OrderedDict()
        for p in d_params:
            _parameter_name = p.partition('_')[2]
            _parameters[_parameter_name] = self.parameters[p]

        _dens_eval= self.obj_density.evaluate(
                r=r,
                parameters=_parameters,
                r_cut=rcut)

        #<--- set the internal attribute
        self.density = copy.deepcopy(_dens_eval)

        return _dens_eval

    def evaluate_embedding(self,
            rho=None,
            parameters=None):
        #<--- check arguments of the function
        if parameters is not None:
            for p in self.parameters:
                self.parameters[p] = parameters[p]
        if rho is not None:
            if isinstance(rho,np.ndarray):
                self.rho = np.copy(rho)
            else:
                raise ValueError("r must be a numpy.ndarray")
            self.rho = np.copy(rho)
        #<--- grab the parameters for the embedding function
        e_params = [p for p in self.parameters if p.startswith('e_')]

        _parameters = OrderedDict()
        for p in e_params:
            _parameter_name = p.partition('_')[2]
            _parameters[_parameter_name] = self.parameters[p]

        #<--- for solving embedding function implicitly from the RoseEquationOfState
        if type(self.obj_embedding) == RoseEquationOfStateEmbeddingFunction:
            if parameters is not None:
                self.obj_embedding.evaluate(
                    rho=self.rho,
                    parameters=parameters, # pass in all parameters not just a subset
                    o_pair=self.obj_pair,
                    o_density=self.obj_density)
            else:
                self.obj_embedding.evaluate(
                    rho=self.rho,
                    r=self.r,
                    parameters=self.parameters, # pass in all parameters not just a subset
                    o_pair=self.obj_pair,
                    o_density=self.obj_density)

        else:
            self.obj_embedding.evaluate(
                rho=self.rho,
                parameters=_parameters)

        #<--- set the internal attribute
        self.embedding = copy.deepcopy(self.obj_embedding.embedding_evaluations)
