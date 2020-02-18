

from collections import OrderedDict

from mexm.io.slurm import SlurmConfiguration

from test__SlurmConfiguration import slurm_config_path
from test__SlurmConfiguration import slurm_lammps_configuration_dict

def dev__set_lammps_configuration__with_args():
    modules = slurm_lammps_configuration_dict['modules']
    run_string = slurm_lammps_configuration_dict['run_string']

    o = SlurmConfiguration()
    o.set_lammps_configuration(
        modules = modules,
        run_string = run_string
    )

    print(
        'type(o.lammps_configuration):{}'.format(
            type(o.lammps_configuration)
        )
    )

    print('o.lammps_configuration:')
    for k,v in o.lammps_configuration.items():
        print('\t{}:{}'.format(k,v))

def test__set_lammps_configuration__with_args():
    modules = slurm_lammps_configuration_dict['modules']
    run_string = slurm_lammps_configuration_dict['run_string']

    o = SlurmConfiguration()
    o.set_lammps_configuration(
        modules = modules,
        run_string = run_string
    )

    assert isinstance(o.lammps_configuration, OrderedDict)

def dev__set_lammps_configuration__with_kwargs():
    o = SlurmConfiguration()
    o.set_lammps_configuration(**slurm_lammps_configuration_dict)

    print(
        'type(o.lammps_configuration):{}'.format(
            type(o.lammps_configuration)
        )
    )

    print('o.lammps_configuration:')
    for k,v in o.lammps_configuration.items():
        print('\t{}:{}'.format(k,v))

def test__set_lammps_configuration__with_kwargs():
    o = SlurmConfiguration()
    o.set_lammps_configuration(**slurm_lammps_configuration_dict)

    assert isinstance(o.lammps_configuration, OrderedDict)

if __name__ == "__main__":
    dev__set_lammps_configuration__with_args()
    dev__set_lammps_configuration__with_kwargs()
