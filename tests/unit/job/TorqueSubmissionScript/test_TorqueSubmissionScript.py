import pytest
import os
from mexm.job.torque import TorqueSubmissionScript

kwargs = {
    'account':'PAA0028',
    'walltime':72,
    'n_nodes':1,
    'ppn':40,
    'jobname':'Si_job_name',
    'errpath':'job.err',
    'stdpath':'job.out',
    'modules':['intel/19.0.5', 'intelmpi/2019.3'],
    'cmd':'mpiexec $VASP_STD_BIN > vasp.out'
}

@pytest.fixture
def objTorqueSubmissionScript():
    obj = TorqueSubmissionScript()
    return obj

def test_wall_time_to_string(objTorqueSubmissionScript):
    walltime_str = objTorqueSubmissionScript.walltime_to_string(72)
    print(walltime_str)
    assert walltime_str == "72:00:00"    

def test__header_section_to_string(objTorqueSubmissionScript):
    kwargs = {
        'account':'PAA0028',
        'walltime':72,
        'n_nodes':1,
        'ppn':40,
        'jobname':'Si_job_name',
        'errpath':'job.err',
        'stdpath':'job.out',
    }
    obj = objTorqueSubmissionScript
    assert isinstance(obj.header_section_to_string(**kwargs), str)

def test__write():
    path = 'runjob.sh'
    obj = TorqueSubmissionScript(**kwargs)
    obj.write(path=path)

    assert os.path.isfile(path)
    
def dev__wall_time_to_string():
    objTorqueSubmissionScript = TorqueSubmissionScript()
    walltime_str = objTorqueSubmissionScript.walltime_to_string(72)
    print(walltime_str)

def dev__header_section_to_string():
    kwargs = {
        'account':'PAA0028',
        'walltime':72,
        'n_nodes':1,
        'ppn':40,
        'jobname':'Si_job_name',
        'errpath':'job.err',
        'stdpath':'job.out',
    }
    obj = TorqueSubmissionScript(**kwargs)
    print(obj.header_section_to_string(**kwargs))

def dev__module_section_to_string():
    obj = TorqueSubmissionScript(**kwargs)
    print(
        obj.module_section_to_string(
            modules=['intel/19.0.5', 'intelmpi/2019.3']
        )
    )
    
if __name__ == "__main__":
    obj = TorqueSubmissionScript(**kwargs)
    print(obj.write(path='runjob.sh'))