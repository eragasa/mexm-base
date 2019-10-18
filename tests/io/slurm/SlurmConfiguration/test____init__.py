import pytest
from mexm.io.slurm import SlurmConfiguration

def dev____init____no_args():
    slurm_configuration = SlurmConfiguration()
    print(slurm_configuration)

def test____init____no_args():
    slurm_configuration = SlurmConfiguration()
