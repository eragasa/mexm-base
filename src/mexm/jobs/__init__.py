from abc import ABC
from abc import abstractmethod

class JobSubmissionManager(ABC):

    @abstractmethod
    def submit_job(self, simulation_path: str, submission_script_path: str):
        raise NotImplementedError

    @abstractmethod
    def get_job_info(self, jobid='all', username=None):
        raise NotImplementedError

from mexm.jobs.torque import TorqueJobSubmissionManager
