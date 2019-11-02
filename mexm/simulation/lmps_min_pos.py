import os,copy
from collections import OrderedDict
from mexm.io.vasp import Poscar
from mexm.simulation import LammpsSimulation
from mexm.simulation import PositionMinimization

class LammpsPositionMinimization(LammpsSimulation, PositionMinimization):
    simulation_type = 'lammps_min_pos'
    is_base_class = False
    results_name = [
        'toten', 'natoms',
        'a11', 'a12', 'a13', 'a21', 'a22', 'a23', 'a31', 'a32', 'a33',
        'totpress',
        'p11', 'p12', 'p13', 'p21', 'p22', 'p23', 'p31', 'p32', 'p33'

    ]
    """ Class for LAMMPS structural minimization

    This data class defines additional attributes and methods necessary to
    interact with the Workflow manager.

    Args:
        name (str)
        simulation_path (str)
        structure_path (str)
        bulk_structure_name (str)

    Attributes:
        bulk_structure_name (str)
        bulk_structure_path (str)
        config_map
    """
    def __init__(self,
                 name,
                 simulation_path,
                 structure_path,
                 bulk_structure_name=None):
        _task_type = 'lmps_min_pos'

        self.bulk_structure_name = None
        self.bulk_structure_path = None
        self.bulk_structure_lattice = None


        LammpsSimulation.__init__(self,
                                  name=name,
                                  simulation_path=simulation_path,
                                  structure_path=structure_path,
                                  bulk_structure_name=bulk_structure_name)

    def postprocess(self):
        LammpsSimulation.postprocess(self)

    def lammps_input_file_to_string(self):
        str_out = "".join([\
                self._lammps_input_initialization_section(),
                self._lammps_input_create_atoms(),
                self._lammps_input_define_potential(),
                self._lammps_input_run_minimization(),
                self._lammps_input_out_section()])
        return(str_out)

    def on_init(self,configuration=None,results=None):
        LammpsSimulation.on_init(self,configuration=configuration)

        if 'bulk_structure' in configuration:
            self.bulk_structure_name = configuration['bulk_structure']
            self.bulk_structure_path = configuration['bulk_structure_filename']
            self.bulk_structure_lattice = OrderedDict()

            _lattice_parameter_variables = [
                    'lmps_min_all.a11',
                    'lmps_min_all.a12',
                    'lmps_min_all.a13',
                    'lmps_min_all.a21',
                    'lmps_min_all.a22',
                    'lmps_min_all.a23',
                    'lmps_min_all.a31',
                    'lmps_min_all.a32',
                    'lmps_min_all.a33']

            self.bulk_lattice_components = OrderedDict()
            for k in _lattice_parameter_variables:
                _k = '{}.{}'.format(self.bulk_structure_name,k)
                self.bulk_lattice_components[_k] = None

    def on_config(self,configuration,results=None):
        if self.bulk_structure_name is not None:
            for k,v in results.items():
                if k in self.bulk_lattice_components:
                    self.bulk_lattice_components[k] = v
        LammpsSimulation.on_config(self,configuration=None,results=None)

    def get_conditions_ready(self):
        LammpsSimulation.get_conditions_ready(self)

        if self.bulk_structure_name is not None:
            _is_components_exist = []
            for k,v in self.bulk_lattice_components.items():
                _is_components_exist.append(v is not None)
            _all_components_exist = all(_is_components_exist)
            self.conditions_READY['bulk_lattice_components'] =\
                    _all_components_exist

    def on_ready(self,configuration=None,results=None):
        if self.bulk_structure_name is not None:
            self.__modify_structure(results=results)
        LammpsSimulation.on_ready(self,configuration=configuration)

    def __modify_structure(self,results):
        assert isinstance(results,dict)
        #_ideal_structure_name = self.ideal_structure_name
        a11_n = '{}.lmps_min_all.a11'.format(self.bulk_structure_name)
        a12_n = '{}.lmps_min_all.a12'.format(self.bulk_structure_name)
        a13_n = '{}.lmps_min_all.a13'.format(self.bulk_structure_name)
        a21_n = '{}.lmps_min_all.a21'.format(self.bulk_structure_name)
        a22_n = '{}.lmps_min_all.a22'.format(self.bulk_structure_name)
        a23_n = '{}.lmps_min_all.a23'.format(self.bulk_structure_name)
        a31_n = '{}.lmps_min_all.a31'.format(self.bulk_structure_name)
        a32_n = '{}.lmps_min_all.a32'.format(self.bulk_structure_name)
        a33_n = '{}.lmps_min_all.a33'.format(self.bulk_structure_name)
        a11 = self.bulk_lattice_components[a11_n]
        a12 = self.bulk_lattice_components[a12_n]
        a13 = self.bulk_lattice_components[a13_n]
        a0 = (a11*a11+a12*a12+a13*a13)**0.5
        self.structure.a0 = a0


    def on_post(self,configuration=None):
        self.__getresults__from_lammps_outputfile()
        LammpsSimulation.on_post(self,configuration=configuration)

    def __getresults__from_lammps_outputfile(self):
        _filename = os.path.join(
                self.simulation_path,
                'lammps.out')
        with open(_filename,'r') as f:
            lines = f.readlines()

        _variables = [
                'tot_energy',
                'num_atoms',
                'a11','a12','a13','a22','a23','a33',
                'tot_press',
                'pxx', 'pyy', 'pzz', 'pxy', 'pxz', 'pyz',
                ]
        results_ = OrderedDict()

        for i,line in enumerate(lines):
            for name in _variables:
                if line.startswith('{} = '.format(name)):
                    results_[name] = float(line.split('=')[1].strip())

                if line.startswith('ERROR:'):
                    print('name:{}'.format(name))
                    print('line:{}'.format(line.strip))
                    raise NotImplementedError

        name_ = self.name
        self.results = OrderedDict()
        self.results['{}.{}'.format(name_,'toten')] = results_['tot_energy']
        self.results['{}.{}'.format(name_,'natoms')] = results_['num_atoms']
        # this only works for orthogonal cells
        self.results['{}.{}'.format(name_,'a11')] = results_['a11']
        self.results['{}.{}'.format(name_,'a12')] = results_['a12']
        self.results['{}.{}'.format(name_,'a13')] = results_['a13']
        self.results['{}.{}'.format(name_,'a21')] = 0
        self.results['{}.{}'.format(name_,'a22')] = results_['a22']
        self.results['{}.{}'.format(name_,'a23')] = results_['a23']
        self.results['{}.{}'.format(name_,'a31')] = 0
        self.results['{}.{}'.format(name_,'a32')] = 0
        self.results['{}.{}'.format(name_,'a33')] = results_['a33']
        self.results['{}.{}'.format(name_,'totpress')] = results_['tot_press']
        self.results['{}.{}'.format(name_,'p11')] = results_['pxx']
        self.results['{}.{}'.format(name_,'p12')] = results_['pxy']
        self.results['{}.{}'.format(name_,'p13')] = results_['pxz']
        self.results['{}.{}'.format(name_,'p21')] = results_['pxy']
        self.results['{}.{}'.format(name_,'p22')] = results_['pyy']
        self.results['{}.{}'.format(name_,'p23')] = results_['pyz'] #pyz=pzy
        self.results['{}.{}'.format(name_,'p31')] = results_['pxz'] #pxz=pzx
        self.results['{}.{}'.format(name_,'p32')] = results_['pyz']
        self.results['{}.{}'.format(name_,'p33')] = results_['pzz']

    def _lammps_input_run_minimization(self):
        str_out = (
            '# ---- define settings\n'
            'compute eng all pe/atom\n'
            'compute eatoms all reduce sum c_eng\n'
            '\n'
            '# ---- run minimization\n'
            'reset_timestep 0\n'
            'thermo 1\n'
            'thermo_style custom step pe lx ly lz xy xz yz press pxx pyy pzz pxy pxz pyz c_eatoms\n'
            'min_style cg\n'
            'minimize 1e-20 1e-20 1000 100000\n'
            '\n'
            )
        return str_out
