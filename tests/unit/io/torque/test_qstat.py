import pytest
import distutils

from abc import ABC
from abc import ABCMeta
from abc import abstractmethod

ERRMSG_NOT_IMPLEMENTED = "You should implement this message"

class Job(ABC): pass
class SerialJob(Job): pass
class MpiJob(): pass
class AbstractSerialJob(): pass
class AbstractMpiJob(AbstractJob):
    __metaclass__ = ABCMeta

    def __init__(self): pass

class AbstractJobFactory(): pass
class SerialJobFactory(AbstractJobFactory): pass
    factories = {}

class MpiJobFactory(AbstractJobFactory):
    factories = {
        'slurm':SlurmJob
    }
class JobFactory(AbstractJobFactory):
class AbstractSubmissionManager:
    __metaclass__ = ABCMeta

    @abstractmethod
    def submit_job(self):
        raise NotImplementedError(ERRMSG_NOT_IMPLEMENTED)
class SubmissionManager(AbstractSubmissionManager):

class AbstractJobRequester():
    


    self,
    simulation: Simulation
    simulation_path: str,
    n_cores: int,
    n_nodes: int

class HpcCluster(ABC):
    w

class TorqueHpcCluster(HpcCluster):
    self __init__(self):
        super().__init__()

class TorqueMpiJobRequester(MpiJobRequester):
    def request_job(
        self,
        simulation: Simulation
        simulation_path: str,
        n_cores: int,
        n_nodes: int
    )

class TorqueSubmissionManager(SubmissionManager):
    def submit_job(
        self,
        job: MpiJob
    ):

        raise NotImplementedError(ERRMSG_NOT_IMPLEMENTED)
    
class SubmissionManagerFactory(AbstractJobFactory):
    factories = {
        'slurm':SlurmSubmissionManager
    }

