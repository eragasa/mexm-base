import time
from copy import deepcopy
from collections import OrderedDict

SimulationMap = OrderedDict()
SimulationMap['lmps_min_all'] = OrderedDict()
SimulationMap['lmps_min_all']['module'] = 'mexm.simulation.lammps'
SimulationMap['lmps_min_all']['class'] = 'LammpsStructuralMinimization'
SimulationMap['lmps_min_pos'] = OrderedDict()
SimulationMap['lmps_min_pos']['module'] = 'mexm.simulation.lammps'
SimulationMap['lmps_min_pos']['class'] = 'LammpsPositionMinimization'
SimulationMap['lmps_min_none'] = OrderedDict()
SimulationMap['lmps_min_none']['module'] = 'mexm.simulation.lammps'
SimulationMap['lmps_min_none']['class'] = 'LammpsStaticCalculations'
SimulationMap['lmps_min_sf'] = OrderedDict()
SimulationMap['lmps_min_sf']['module'] = 'mexm.simulation.lammps'
SimulationMap['lmps_min_sf']['class'] = 'LammpsStackingFaultMinimization'
SimulationMap['lmps_elastic'] = OrderedDict()
SimulationMap['lmps_elastic']['module'] = 'mexm.simulation.lammps'
SimulationMap['lmps_elastic']['class'] = 'LammpsElasticCalculation'
SimulationMap['lmps_npt'] = OrderedDict()
SimulationMap['lmps_npt']['module'] = 'mexm.simulation.lammps'
SimulationMap['lmps_npt']['class']= 'LammpsNptSimulation'
SimulationMap['lmps_neb'] = OrderedDict()
SimulationMap['lmps_neb']['module'] = 'mexm.simulation.lammps'
SimulationMap['lmps_neb']['class'] = 'LammpsNebCalculation'
SimulationMap['gulp_gamma_phonons'] = OrderedDict()
SimulationMap['gulp_gamma_phonons']['module'] = 'mexm.simulation.gulp'
SimulationMap['gulp_gamma_phonons']['class'] = 'GulpGammaPointPhonons'

class SimulationManager(object):
    def __init__(self, base_path):
        self.base_path = base_path
        self.structures = None
        self.simulations = None
        self.results = None

        self.max_time_per_simulation = 100.
        self.loop_sleep_time = 0.1
    def configure(self, simulations, structures):
        self.simulations = deepcopy(simulations)
        self.structures = deepcopy(structures)

    def __all_simulations_finished(self, simulations):
        statuses = [v.status in ['FINISHED', 'ERROR'] for v in simulations.values()]
        return all(statuses)


    def evaluate_simulations(self,
                             parameters,
                             potential,
                             max_time_per_simulation=None):

        self.results = OrderedDict()
        configuration_ = {
            'potential':potential,
            'parameters':parameters
        }

        start_time = time.time()
        while not self.__all_simulations_finished(self.obj_Task):
            time_elapsed = time.time() - start_time
            if time_elapsed > max_time_per_simulation:
                for sim_k, sim_v in self.simulations.items():
                    self.kill_simulation(obj_simulation=sim_v['obj_simulation'])
            raise MexmSimulationManagerError(
                "simulation time exceeded",
                parameters=parameters
            )

        for sim_k, sim_v in self.simulations.items():
            obj_simulation = sim_v['obj_simulation']
            obj_simulation.update_status()

            if 'bulk_structure' in self.simulations[sim_k]:
                structure_name = self.simulation[sim_k]['bulk_structure']
                structure_path = self.get_structure_path(
                        structure_name=structure_name
                )
                configuration_ = {
                    'potential':potential,
                    'parameters':parameters,
                    'bulk_structure':structure_name,
                    'bulk_structure_path':structure_path
                }


            if obj_simulation.status == 'INIT':
                obj_simulation.on_init(configuration=configuration_)
            elif obj_simulation.status == 'CONFIG':
                try:
                    obj_simulation.on_config(configuration=configuration_,
                                             results=self.results)
                except TypeError as e:
                    obj_simulation.on_config(configuration=configuration_)
            elif obj_simulation.status == 'READY':
                obj_simulation.on_ready(results=self.results)
            elif obj_simulation.status == 'POST':
                obj_simulation.on_post()
                results = obj_simulation.results
                try:
                    for k, v in obj_simulation.results.items():
                        self.results[k] = v
                except AttributeError as e:
                    print('sim_k:{}'.format(sim_k))
                    print('sim_v:{}'.format(sim_v))
                    raise
            elif obj_simulation.status == "FINISHED":
                obj_simulation.on_finished()
            elif obj_simulation.status ==  "ERROR":
                obj_simulation.on_error()
            else:
                MexmSimulationManagerError(
                    "unknown status:{}".format(obj_simulation.status)
                )

    def kill_simulation(self, obj_simulation):
        try:
            obj_simulation.process.kill()
        except:
            pass

    def get_structure_path(self, structure_name):
        structure_directory = self.structures['structure_directory']
        structure_filename = self.structures['structures'][structure_name]
        structure_path = os.path.join(structure_directory, structure_filename)
        return structure_path
