import os, shutil

from mexm.exceptions import MexmException

class MexmSimulationException(MexmException): pass

class Simulation():
    states = ['INIT','CONFIG','READY','RUNNING','POST','FINISHED','ERROR']
    def __init__(self,
                 name,
                 simulation_path):
        self.name = name
        self.simulation_path = simulation_path
        self.create_simulation_directory()

        self.status = None

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
        if not all([v for k,v in self.conditions__INIT.items()]):
            return

        self.get_conditions_config()
        if not all([v for k,v in self.conditions__CONFIG.items()]):
            self.status = 'INIT'
            return

        self.get_conditions_ready()
        if not all([v for k,v in self.conditions__READY.items()]):
            self.status = "CONFIG"
            return

        self.get_conditions_running()
        if not all([v for k,v in self.conditions_RUNNING.items()]):
            self.status = "READY"
            return

        self.get_conditions_finished()
        if not all([v for k,v in self.conditions_POST.ITEMS()]):
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
