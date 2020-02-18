import pytest

import sys, os

from mexm.io.slurm import SlurmConfiguration
from mexm.io.slurm import SlurmSubmissionScript

slurm_configuration = SlurmConfiguration()
slurm_configuration.set_slurm_configuration(
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
slurm_configuration.set_vasp_configuration(
    modules=['intel/2016.0.19', 'impi'],
    run_string='srun --mpi=pmi2 $VASP_BIN > vasp.log'

)
slurm_configuration.set_phonts_configuration(
    modules=['intel/2016.0.19', 'impi'],
    run_string='srun --mpi=pmi2 $PHONTS_BIN > phonts.log'
)
slurm_configuration.set_lammps_configuration(
    modules=['openmpi'],
    run_string='srun --mpi=pmi2 $LAMMPS_SERIAL_BIN > lammps.out'
)

def dev__SlurmSubmissionScript():

    script = SlurmSubmissionScript(configuration=slurm_configuration)
    script_str = script.slurm_script_to_string()
    print(script_str)

    slurm_script_path = "runjob.slurm"
    if os.path.isfile(slurm_script_path):
        os.remove(slurm_script_path)
    script.write(path=slurm_script_path)
    assert os.remove
    os.remove(slurm_script_path)

if __name__ == "__main__":
    dev__SlurmSubmissionScript()
