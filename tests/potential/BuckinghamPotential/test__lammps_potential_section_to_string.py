import pytest
from collections import OrderedDict
from mexm.potential import BuckinghamPotential

def test__lammps_potential_section_to_string():
    symbols = ['Mg', 'O']
    parameters = OrderedDict([
        ('cutoff',12.0),
        ('Mg_chrg', +2.),
        ('O_chrg', -2.),
        ('MgMg_A',10000.),
        ('MgMg_rho', 500.),
        ('MgMg_C', 200.),
        ('MgMg_cutoff', 12.),
        ('MgO_A',10000.),
        ('MgO_rho', 500.),
        ('MgO_C', 200.),
        ('MgO_cutoff', 12.),
        ('OO_A',10000.),
        ('OO_rho', 500.),
        ('OO_C', 200.),
        ('OO_cutoff', 12.)
    ])

    potential = BuckinghamPotential(symbols=symbols)
    s = potential.lammps_potential_section_to_string(parameters=parameters)
    assert isinstance(s, str)

def dev__lammps_potential_section_to_string():
    symbols = ['Mg', 'O']
    potential = BuckinghamPotential(symbols=symbols)
    parameters = OrderedDict([
        ('cutoff',12.0),
        ('Mg_chrg', +2.),
        ('O_chrg', -2.),
        ('MgMg_A',10000.),
        ('MgMg_rho', 500.),
        ('MgMg_C', 200.),
        ('MgMg_cutoff', 12.),
        ('MgO_A',10000.),
        ('MgO_rho', 500.),
        ('MgO_C', 200.),
        ('MgO_cutoff', 12.),
        ('OO_A',10000.),
        ('OO_rho', 500.),
        ('OO_C', 200.),
        ('OO_cutoff', 12.)
    ])

    s = potential.lammps_potential_section_to_string(parameters=parameters)
    print(80*'-')
    print('{:^80}'.format('LAMMPS POTENTIAL SECTION'))
    print(80*'-')
    print(s)
    
if __name__ == "__main__":
    dev__lammps_potential_section_to_string()
