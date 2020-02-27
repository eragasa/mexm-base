import pytest

import os
import sys
import subprocess
from mexm.jobs import TorqueJobSubmissionManager

@pytest.fixture
def objJobSubmissionManager():
    objJobSubmissionManager = TorqueJobSubmissionManager()
    return objJobSubmissionManager

def test_init():
    objJobSubmissionManager = TorqueJobSubmissionManager()

def test_submitjob(objJobSubmissionManager):
    simulation_path = "."
    submission_script_path = 'runjob_pitzer_debug.sh'  
    std_out = objJobSubmissionManager.submit_job(
        simulation_path = simulation_path,
        submission_script_path = submission_script_path
    )
    print(std_out)

def test_cancel_job(objJobSubmissionManager):
    simulation_path = "."
    submission_script_path = 'runjob_pitzer_debug.sh'  
    std_out = objJobSubmissionManager.submit_job(
        simulation_path = simulation_path,
        submission_script_path = submission_script_path
    )
    jobid = std_out.split('.')[0] 
    objJobSubmissionManager.cancel_job(jobid=jobid)

def test_cancel_job__bad_jobid(objJobSubmissionManager):
    simulation_path = "."
    submission_script_path = 'runjob_pitzer_debug.sh'  

    jobid = 'badjobid'
    objJobSubmissionManager.cancel_job(jobid=jobid)
    'qdel: nonexistent job id: 1'
if __name__ == "__main__":
    objJobSubmissionManager = TorqueJobSubmissionManager()
    
    simulation_path = "."
    submission_script_path = 'runjob_pitzer_debug.sh'  
    std_out = objJobSubmissionManager.submit_job(
        simulation_path = simulation_path,
        submission_script_path = submission_script_path
    )
    print(std_out)
