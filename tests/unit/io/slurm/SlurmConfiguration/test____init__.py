import pytest
from mexm.io.slurm import SlurmConfiguration

from test__SlurmConfiguration import slurm_configuration_dict

def dev____init____no_args():
    slurm_configuration = SlurmConfiguration()
    print(slurm_configuration)

def test____init____no_args():
    slurm_configuration = SlurmConfiguration()

def test__initialize_from_dict():
    o = SlurmConfiguration.initialize_from_dict(slurm_configuration_dict)

if __name__ == "__main__":
    dev____init____no_args()
