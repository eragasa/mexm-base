import pytest

from collections import OrderedDict

from mexm.io.slurm import SlurmConfiguration

from test__SlurmConfiguration import slurm_config_path
from test__SlurmConfiguration import slurm_vasp_configuration_dict

def dev__set_vasp_configuration__with_args():
    modules = slurm_vasp_configuration_dict['modules']
    run_string = slurm_vasp_configuration_dict['run_string']

    o = SlurmConfiguration()
    o.set_vasp_configuration(
        modules = modules,
        run_string = run_string
    )

    print(
        'type(o.vasp_configuration):{}'.format(
            type(o.vasp_configuration)
        )
    )

    print('o.vasp_configuration:')
    for k,v in o.vasp_configuration.items():
        print('\t{}:{}'.format(k,v))

def test__set_vasp_configuration__with_args():
    modules = slurm_vasp_configuration_dict['modules']
    run_string = slurm_vasp_configuration_dict['run_string']

    o = SlurmConfiguration()
    o.set_vasp_configuration(
        modules = modules,
        run_string = run_string
    )

    assert isinstance(o.vasp_configuration, OrderedDict)

def dev__set_vasp_configuration__with_kwargs():
    o = SlurmConfiguration()
    o.set_vasp_configuration(**slurm_vasp_configuration_dict)

    print(
        'type(o.vasp_configuration):{}'.format(
            type(o.vasp_configuration)
        )
    )

    print('o.vasp_configuration:')
    for k,v in o.vasp_configuration.items():
        print('\t{}:{}'.format(k,v))

def test__set_vasp_configuration__with_kwargs():
    o = SlurmConfiguration()
    o.set_vasp_configuration(**slurm_vasp_configuration_dict)

    assert isinstance(o.vasp_configuration, OrderedDict)

if __name__ == "__main__":
    dev__set_vasp_configuration__with_args()
    dev__set_vasp_configuration__with_kwargs()
