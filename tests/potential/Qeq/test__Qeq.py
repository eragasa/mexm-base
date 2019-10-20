import pytest
from mexm.potential.qeq import Qeq

# https://github.com/lammps/lammps/blob/master/examples/qeq/in.qeq.buck
case_mgo = {
    'symbols':['Mg', 'O'],
    'lammps_fix_id':2,
    'lammps_group_id':'all',
    'qfile_path':'param.qeq',
    'parameter_names':{
        'qeq_Nevery':1,
        'qeq_cutoff':12.,
        'qeq_tolerance':1.0e-6,
        'qeq_maxiter':100,
        'Mg_qeq_chi': 0.00000,
        'Mg_qeq_eta': 7.25028,
        'Mg_qeq_gamma': 0.01,
        'Mg_qeq_zeta': 0.772871,
        'Mg_qeq_qcore': 0.000000,
        'O_qeq_chi': 11.26882,
        'O_qeq_eta': 15.37920,
        'O_qeq_gamma': 0.01,
        'O_qeq_zeta': 0.243072,
        'O_qeq_qcore': 0.000000
    }
}

def dev__Qeq():
    symbols = ['Mg', 'O']

    o = Qeq(symbols=symbols)
    print('o.potential_type:{}'.format(o.potential_type))
    print('o.parameter_names_global:{}'.format(o.parameter_names_global))
    print('o.parameter_names_1body:{}'.format(o.parameter_names_1body))

    print('o.parameter_names:')
    for k in o.parameter_names:
        print('\t{}'.format(k))

    print('o.lammps_fix_qeq_to_string()')
    print(o.lammps_fix_qeq_to_string())
def test____init__():
    symbols = ['Mg', 'O']

    o = Qeq(symbols=symbols)
    assert isinstance(o.symbols, list)
    assert o.symbols == symbols

def test__get_parameter_names():
    symbols = ['Mg', 'O']
    assert isinstance(Qeq.get_parameter_names(symbols=symbols), list)

if __name__ == "__main__":
    dev__Qeq()
