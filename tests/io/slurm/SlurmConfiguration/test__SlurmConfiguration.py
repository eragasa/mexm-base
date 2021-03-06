import pytest
import os

from collections import OrderedDict

from mexm.io.slurm import SlurmConfiguration

slurm_config_path = 'slurm_config.yaml'
slurm_configuration_dict = OrderedDict([
    ('job_name', 'default_job'),
    ('qos', 'phillpot-b'),
    ('mail_type', 'END'),
    ('mail_name', 'eragasa@ufl.edu'),
    ('ntasks', 16),
    ('output_path', 'job.out'),
    ('error_path', 'job.err'),
    ('time', '1:00:00'),
    ('memory', '4gb')
])
slurm_vasp_configuration_dict = OrderedDict([
    ('modules', ['intel/2016.0.19', 'impi']),
    ('run_string', 'srun --mpi=pmi2 $VASP_BIN > vasp.log')
])
slurm_phonts_configuration_dict = OrderedDict([
    ('modules', ['intel/2016.0.19', 'impi']),
    ('run_string', 'srun --mpi=pmi2 $PHONTS_BIN > phonts.log')
])
slurm_set_lammps_configuration_dict = OrderedDict([
    ('modules', ['openmpi']),
    ('run_string', 'srun --mpi=pmi2 $LAMMPS_SERIAL_BIN > lammps.out')
])



def dev__SlurmConfiguration():
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
    o.set_vasp_configuration(
        modules=['intel/2016.0.19', 'impi'],
        run_string='srun --mpi=pmi2 $VASP_BIN > vasp.log'

    )
    o.set_phonts_configuration(
        modules=['intel/2016.0.19', 'impi'],
        run_string='srun --mpi=pmi2 $PHONTS_BIN > phonts.log'
    )
    o.set_lammps_configuration(
        modules=['openmpi'],
        run_string='srun --mpi=pmi2 $LAMMPS_SERIAL_BIN > lammps.out'
    )

    slurm_configuration.write('slurm_config.yaml')
    slurm_configuration.read('slurm_config.yaml')
    os.remove(slurm_config_path)

if __name__ == "__main__":
    dev__SlurmConfiguration()
