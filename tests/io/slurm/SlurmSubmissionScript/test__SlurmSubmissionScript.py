import pytest

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

def dev__SlurmSubmissionScript__empty():
    script = SlurmSubmissionScript()
