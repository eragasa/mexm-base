import os,copy
from collections import OrderedDict
from mexm.simulation import LammpsSimulation, StaticCalculation

class LammpsStaticCalculation(LammpsSimulation, StaticCalculation):
    simulation_type = 'lammps_min_none'
    is_base_class = False
    results_names = [
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
        config
        config_map
    """
    def __init__(self,
                 name,
                 simulation_path,
                 structure_path,
                 bulk_structure_name=None):

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

    def on_config(self,configuration,results=None):
        LammpsSimulation.on_config(self,configuration=None,results=results)

    def get_conditions_ready(self):
        LammpsSimulation.get_conditions_ready(self)
        a0_name = '{}.{}.a0'.format(self.bulk_structure_name, 'lmps_min_all')
        try:
            self.conditions_READY['bulk_structure_results_available'] \
                = a0_name in self.results
        except TypeError as e:
            if self.results is None:
                self.conditions_READY['bulk_structure_results_available'] \
                    = False
            else:
                raise
        return self.conditions_READY

    def on_ready(self,configuration, results=None):
        self.results = deepcopy(results)
        LammpsSimulation.on_ready(self,
                                  configuration=configuration,
                                  results=self.results)

    def modify_structure_file(self, results):
        a0_name = '{}.{}.a0'.format(self.bulk_structure_name, 'lmps_min_all')
        self.lammps_structure.a0 = results[a0_name]

    def on_post(self,configuration=None):
        self.__get_results_from_lammps_outputfile()
        LammpsSimulation.on_post(self,configuration=configuration)

    def on_ready(self,configuration=None,results=None):
        LammpsSimulation.on_ready(
                self,
                configuration=configuration,
                results=results)

    def __get_results_from_lammps_outputfile(self):
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
        _results = OrderedDict()

        for i,line in enumerate(lines):
            for name in _variables:
                if line.startswith('{} = '.format(name)):
                    _results[name] = float(line.split('=')[1].strip())

                if line.startswith('ERROR:'):
                    print('name:{}'.format(name))
                    print('line:{}'.format(line.strip))
                    raise NotImplementedError

        _task_name = self.task_name
        self.results = OrderedDict()
        self.results['{}.{}'.format(_task_name,'toten')] = _results['tot_energy']
        self.results['{}.{}'.format(_task_name,'natoms')] = _results['num_atoms']
        # this only works for orthogonal cells
        self.results['{}.{}'.format(_task_name,'a11')] = _results['a11']
        self.results['{}.{}'.format(_task_name,'a12')] = _results['a12']
        self.results['{}.{}'.format(_task_name,'a13')] = _results['a13']
        self.results['{}.{}'.format(_task_name,'a21')] = 0
        self.results['{}.{}'.format(_task_name,'a22')] = _results['a22']
        self.results['{}.{}'.format(_task_name,'a23')] = _results['a23']
        self.results['{}.{}'.format(_task_name,'a31')] = 0
        self.results['{}.{}'.format(_task_name,'a32')] = 0
        self.results['{}.{}'.format(_task_name,'a33')] = _results['a33']
        self.results['{}.{}'.format(_task_name,'totpress')] = _results['tot_press']
        self.results['{}.{}'.format(_task_name,'p11')] = _results['pxx']
        self.results['{}.{}'.format(_task_name,'p12')] = _results['pxy']
        self.results['{}.{}'.format(_task_name,'p13')] = _results['pxz']
        self.results['{}.{}'.format(_task_name,'p21')] = _results['pxy']
        self.results['{}.{}'.format(_task_name,'p22')] = _results['pyy']
        self.results['{}.{}'.format(_task_name,'p23')] = _results['pyz'] #pyz=pzy
        self.results['{}.{}'.format(_task_name,'p31')] = _results['pxz'] #pxz=pzx
        self.results['{}.{}'.format(_task_name,'p32')] = _results['pyz']
        self.results['{}.{}'.format(_task_name,'p33')] = _results['pzz']

    def _lammps_input_run_minimization(self):
        str_out = (
            '# ---- define settings\n'
            'compute eng all pe/atom\n'
            'compute eatoms all reduce sum c_eng\n'
            '# ---- run minimization\n'
            'reset_timestep 0\n'
            'thermo 10\n'
            'thermo_style custom step pe lx ly lz xy xz yz press pxx pyy pzz pxy pxz pyz c_eatoms\n'
            'run 0\n'
            )
        return str_out
