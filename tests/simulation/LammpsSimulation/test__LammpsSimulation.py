import pytest
import os, shutil
from mexm.simulation import LammpsSimulation

def test____init__():
    kwargs = {
        'name':'test_name',
        'simulation_path':'simulation_path',
        'task_requires':None,
        'structure_path':os.path.join('resources','POSCAR'),
    }

    simulation = LammpsSimulation(**kwargs)
    assert not simulation.is_fullauto
    assert simulation.potential is None
    assert simulation.lammps_script is None
    assert simulation.structure_path == kwargs['structure_path']

    assert simulation.lammps_input_path == 'lammps.in'
    assert simulation.lammps_output_path == 'lammps.out'
    assert simulation.lammps_structure_path == 'lammps.structure'
    assert simulation.lammps_potentialmod_path == 'potential.mod'
    assert simulation.lammps_setfl_path is None

    try:
        lammps_bin = os.environ['LAMMPS_SERIAL_BIN']
        assert simulation.lammps_bin == os.environ['LAMMPS_SERIAL_BIN']
    except KeyError:
        assert simulation.lammps_bin is None
    assert os.path.isdir(kwargs['simulation_path'])

    shutil.rmtree(kwargs['simulation_path'])

def test__configure_potential_from_OrderedDict():
    potential_config = OrderedDict([
        ('potential_type','buckingham'),
        ('symbols',['Mg', 'O'])
    ])

if __name__ == "__main__":
    kwargs = {
        'name':'test_name',
        'simulation_path':'simulation_path',
        'task_requires':None,
        'structure_path':os.path.join('resources','POSCAR'),
    }

    simulation = LammpsSimulation(**kwargs)

    shutil.rmtree(kwargs['simulation_path'])
