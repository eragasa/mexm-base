from abc import ABC
from abc import abstractmethod

class HpcClusterInformation(ABC):
    def __init__(self):
        self.name = None
        self.cores_per_node = None
        self.ram_per_node = None

class HpcJobInformation(ABC):
    pass

class HpcSubmissionScript(ABC):

    def __init__(self): pass
    @abstractmethod
    def read(self, path):
        raise NotImplementedError

    @abstractmethod
    def write(self, path):
        raise NotImplementedError


class JobSubmissionManager(ABC):

    @abstractmethod
    def submit_job(self, simulation_path: str, submission_script_path: str):
        raise NotImplementedError

    @abstractmethod
    def get_job_info(self, jobid='all', username=None):
        raise NotImplementedError

from mexm.job.torque import TorqueJobSubmissionManager
