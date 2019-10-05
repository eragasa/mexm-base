import pytest
from collections import OrderedDict
from mexm.potential import BuckinghamPotential

def test__static_variables():
    assert isinstance(BuckinghamPotential.one_body_parameters, list)
    assert isinstance(BuckinghamPotential.two_body_parameters, list)
    assert isinstance(BuckinghamPotential.potential_type, str)
    assert isinstance(BuckinghamPotential.is_charge, bool)

    assert BuckinghamPotential.global_parameters == ['cutoff']
    assert BuckinghamPotential.one_body_parameters == ['chrg', 'cutoff']
    assert BuckinghamPotential.two_body_parameters == ['A', 'rho', 'C', 'cutoff']
    assert BuckinghamPotential.potential_type == 'buckingham'
    assert BuckinghamPotential.is_charge


    if BuckinghamPotential.is_charge:
        'chrg' in BuckinghamPotential.one_body_parameters

def test____init____no_args():
    symbols = ['Mg', 'O']

    potential = BuckinghamPotential(symbols=symbols)

    assert isinstance(potential.parameter_names, list)
    assert isinstance(potential.parameters, OrderedDict)

def dev____init____no_args():
    symbols = ['Mg', 'O']
    potential = BuckinghamPotential(symbols=symbols)
    print('parameter_names')
    for pn in potential.parameter_names:
        print('\t{}'.format(pn))

    print('parameters')
    for k,v in potential.parameters.items():
        print('\t{}:{}'.format(k,v))

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

def test__gulp_potential_section_to_string():
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
    s = potential.gulp_potential_section_to_string(parameters=parameters)
    assert isinstance(s, str)

def dev__gulp_potential_section_to_string():
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

    s = potential.gulp_potential_section_to_string(parameters=parameters)
    print(80*'-')
    print('{:^80}'.format('GULP POTENTIAL SECTION'))
    print(80*'-')
    print(s)

if __name__ == "__main__":
    dev____init____no_args()
    dev__lammps_potential_section_to_string()
    dev__gulp_potential_section_to_string()
