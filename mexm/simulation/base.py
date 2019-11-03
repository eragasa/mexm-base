import os, shutil
from copy import deepcopy
from mexm.exception import MexmException

class MexmSimulationException(MexmException): pass

class Simulation():
    is_base_class = True
    states = ['INIT','CONFIG','READY','RUNNING','POST','FINISHED','ERROR']
    def __init__(self,
                 name,
                 simulation_path):
        self.name = name
        self.simulation_path = simulation_path
        self.conditions = {k:{} for k in Simulation.states}

        self.create_simulation_directory()

        self.status = None

    @property
    def conditions_INIT(self): 
        return self.conditions['INIT']

    @conditions_INIT.setter
    def conditions_INIT(self, conditions): 
        self.conditions['INIT'] = deepcopy(conditions)

    @property
    def conditions_CONFIG(self): return self.conditions['CONFIG']

    @conditions_CONFIG.setter
    def conditions_CONFIG(self, conditions):
        self.conditions['CONFIG'] = deepcopy(conditions)

    @property
    def conditions_READY(self): return self.conditions['READY']

    @conditions_READY.setter
    def conditions_READY(self, conditions):
        self.conditions['READY'] = deepcopy(conditions)

    @property
    def conditions_RUNNING(self): return self.conditions['RUNNING']

    @conditions_RUNNING.setter
    def conditions_RUNNING(self, conditions):
        self.conditions['RUNNING'] = deepcopy(conditions)

    @property
    def conditions_POST(self): return self.conditions['POST']

    @conditions_POST.setter
    def conditions_POST(self, conditions):
        self.conditions['POST'] = deepcopy(conditions)

    @property
    def conditions_FINISHED(self): return self.conditions['FINISHED']

    @conditions_FINISHED.setter
    def conditions_FINISHED(self, conditions):
        self.conditions['FINISHED'] = deepcopy(conditions)

    @property
    def conditions_ERROR(self): return self.conditions['ERROR']

    @conditions_ERROR.setter
    def conditions_ERROR(self, conditions):
        self.conditions['ERROR'] = deepcopy(conditions)

    def run(self): raise NotImplementedError

    def create_simulation_directory(self, path=None):
        if path is not None:
            assert isinstance(path, str)
            self.simulation_path = path
        path_ = self.simulation_path

        if os.path.abspath(os.getcwd()) == os.path.abspath(path_):
            raise MexmSimulationException(
                "Cannot set the simulation path to the current working directory"
            )

        if os.path.isdir(path_):
            shutil.rmtree(path_, ignore_errors=True)

        # this is to deal with possible race conditions while deleting directory
        while True:
            try:
                os.mkdir(path_)
                break
            except FileExistsError as e:
                if os.path.isdir(path_):
                    shutil.rmtree(path_, ignore_errors=True)
                    if e.errno != os.errno.EEXIST:
                        raise
                    pass

    def on_update_status(self):
        status_to_method_map = {
            'INIT':self.on_init,
            'CONFIG':self.on_config,
            'READY':self.on_ready,
            'RUNNING':self.on_running,
            'POST':self.on_post,
            'FINISHED':self.on_finished,
            'ERROR':self.on_error
        }
        status_to_method_map[self.status]()

    def on_init(): raise NotImplementedError
    def on_config(): raise NotImplementedError
    def on_ready(): raise NotImplementedError
    def on_running(): raise NotImplementedError
    def on_post(): raise NotImplementedError
    def on_finished(): raise NotImplementedError
    def on_error(): raise NotImplementedError

    def update_status(self):
        self.get_conditions_init()
        assert isinstance(self.conditions_INIT, dict)
        if not all([v for k,v in self.conditions_INIT.items()]):
            return

        self.get_conditions_config()
        if not all([v for k,v in self.conditions_CONFIG.items()]):
            self.status = 'INIT'
            return

        self.get_conditions_ready()
        if not all([v for k,v in self.conditions_READY.items()]):
            self.status = "CONFIG"
            return

        self.get_conditions_running()
        if not all([v for k,v in self.conditions_RUNNING.items()]):
            self.status = "READY"
            return

        self.get_conditions_finished()
        if not all([v for k,v in self.conditions_POST.items()]):
            self.status = "RUNNING"
            return

        self.status = "FINISHED"

    def get_conditions_init(self): raise NotImplementedError
    def get_conditions_config(self): raise NotImplementedError
    def get_conditions_ready(self): raise NotImplementedError
    def get_conditions_running(self): raise NotImplementedError
    def get_conditions_post(self): raise NotImplementedError
    def get_conditions_finished(self): raise NotImplementedError

class AtomicSimulation(Simulation): pass
