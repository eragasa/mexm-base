import pytest
from mexm.qoi import GulpElasticProperties

def dev__GulpElasticProperties__calculated_qoi_names():
    calculated_qoi_names = GulpElasticProperties.calculated_qoi_names
    print(80*'-')
    print('{:^80}'.format('GulpElasticProperties.calculated_qoi_names'))
    print(80*'-')
    for k in calculated_qoi_names:
        print('\t{}'.format(k))

def test__GulpElasticProperties__calculated_qoi_names():
    expected_calculated_qoi_names =[
        'gulp_c11', 'gulp_c12', 'gulp_c13',
        'gulp_c22', 'gulp_c33', 'gulp_c44', 'gulp_c55', 'gulp_c66',
        'gulp_bulk', 'gulp_shear']
    calculated_qoi_names = GulpElasticProperties.calculated_qoi_names
    assert calculated_qoi_names == expected_calculated_qoi_names

def test__GulpElasticProperties__ideal_simulation_type():
    assert GulpElasticProperties.ideal_simulation_type == 'gulp_elastic'

def dev__GulpElasticProperties____init__():
    kwargs = {
        'qoi_name': 'test_gulp_elastic',
        'structures': {'ideal':'MgO_NaCl_unit'}
    }
    o = GulpElasticProperties(**kwargs)

def test__GulpElasticProperties____init__():
    kwargs = {
        'qoi_name': 'test_gulp_elastic',
        'structures': {'ideal':'MgO_NaCl_unit'}
    }
    o = GulpElasticProperties(qoi_name=kwargs['qoi_name'],
                              structures=kwargs['structures'])

def dev__GulpElasticProperties__determine_simulations():
    kwargs = {
        'qoi_name': 'test_gulp_elastic',
        'structures': {'ideal':'MgO_NaCl_unit'}
    }
    o = GulpElasticProperties(**kwargs)
    o.determine_simulations()
    for simulation_name, simulation_info in o.simulation_definitions.items():
        print(simulation_name)
        for k, v in simulation_info.items():
            if v is not None:
                print('\t{:25}{:25}'.format(k, v))

def test__GulpElasticProperties__determine_simulations():
        kwargs = {
            'qoi_name': 'test_gulp_elastic',
            'structures': {'ideal':'MgO_NaCl_unit'}
        }
        expected_simulation_definitions = {
            'ideal': {
                'simulation_name':'{}.{}'.format(
                    kwargs['structures']['ideal'],
                    GulpElasticProperties.ideal_simulation_type
                ),
                'simulation_type':GulpElasticProperties.ideal_simulation_type,
                'simulation_structure':kwargs['structures']['ideal']
            }
        }
        o = GulpElasticProperties(**kwargs)
        o.determine_simulations()

        for sim_name, sim_info in expected_simulation_definitions.items():
            for k, v in sim_info.items():
                assert o.simulation_definitions[sim_name][k] == v

if __name__ == '__main__':
    dev__GulpElasticProperties__calculated_qoi_names()
    dev__GulpElasticProperties____init__()
    dev__GulpElasticProperties__determine_simulations()
