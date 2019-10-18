import pytest

from collections import OrderedDict

from mexm.io.slurm import SlurmConfiguration
from mexm.io.slurm import SlurmSubmissionScript

from test__SlurmSubmissionScript import slurm_configuration

def dev____init____no_args():
    o = SlurmSubmissionScript()
    print("{}:{}".format('type(o.configuration)',
                         type(o.configuration)
                         )
    )


def test____init____no_args():
    o = SlurmSubmissionScript()

def test____init____w_SlurmConfiguration():
    o = SlurmSubmissionScript(configuration=slurm_configuration)
    assert isinstance(o.configuration, SlurmConfiguration)

def test____init____w_OrderedDict():
    obj_config = slurm_configuration.to_dict()
    assert isinstance(obj_config, OrderedDict)

    o = SlurmSubmissionScript(configuration=obj_config)
    assert isinstance(o.configuration, SlurmConfiguration)

if __name__ == "__main__":

    dev____init____no_args()
