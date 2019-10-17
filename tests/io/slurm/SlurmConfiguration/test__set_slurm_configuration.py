import pytest

from mexm.io.slurm import SlurmConfiguration

from test__SlurmConfiguration import slurm_config_path
from test__SlurmConfiguration import slurm_configuration_dict

def dev__set_slurm_configuraion__with_args():
    o = SlurmConfiguration()
    o.set_slurm_configuration(
        job_name='default_job',
        qos='phillpot-b',
        mail_type='END',
        mail_name='eragasa@ufl.edu',
        ntasks='16',
        output_path='job.out',
        error_path='job.err',
        time='1:00:00',
        memory='4gb'
    )

    print('type(slurm_configuration.slurm_configuration):{}'.format(
        type(o.slurm_configuration)
    )'
    for k,v in o.slurm_configuration.items():
        print(k, v)

def dev__set_slurm_configuration__with_kwargs():
    o = SlurmConfiguration():
    o.set_slurm_configuration(**slurm_configuration_dict)

    print('type(slurm_configuration.slurm_configuration):{}'.format(
        type(o.slurm_configuration)
    )'
    for k,v in o.slurm_configuration.items():
        print(k, v)


if __name__ == "__main__":
    dev__set_slurm_configuration__with_args()
    dev__set_slurm_configuration__with_kwargs()
