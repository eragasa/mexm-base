from mexm.qoi import ElasticProperties
from mexm.qoi import LammpsElasticProperties

def test__LammpsElasticProperties____init__():
    qoi_name = 'MgO.lmps_elastic'
    structures_dict = {
        'ideal':'MgO_NaCl_unit'
    }
    o = LammpsElasticProperties(qoi_name=qoi_name,
                                structures=structures_dict)

def test__LammpsElasticProperties__determine_simulations():
    qoi_name = 'MgO.lmps_elastic'
    structures_dict = {
        'ideal':'MgO_NaCl_unit'
    }
    expected_simulation_definitions = {
        'ideal':{
            'simulation_name':'MgO_NaCl_unit.lmps_elastic',
            'simulation_type':'lmps_elastic',
            'simulation_structure':'MgO_NaCl_unit',
            'bulk_structure':None
        }
    }
    o = LammpsElasticProperties(qoi_name=qoi_name,
                                structures=structures_dict)
    o.determine_simulations()
    assert o.qoi_name == 'MgO.lmps_elastic'
    assert o.structures == structures_dict
    for k, v in expected_simulation_definitions['ideal'].items():
        o.simulation_definitions['ideal'][k] = v

def test__LammpsElasticProperties__calculate_qois():
    assert False

def test__LammpsElasticProperties__calculated_qoi_names():
    expected_calculated_qoi_names = [
        'lammps_c11',
        'lammps_c12',
        'lammps_c13',
        'lammps_c22',
        'lammps_c33',
        'lammps_c44',
        'lammps_c55',
        'lammps_c66',
        'lammps_bulk',
        'lammps_shear']
    assert LammpsElasticProperties.calculated_qoi_names \
        == expected_calculated_qoi_names
    assert len(LammpsElasticProperties.calculated_qoi_names)  \
        == len(ElasticProperties.calculated_qoi_names)

if __name__ == "__main__":

    calculated_qoi_names = LammpsElasticProperties.calculated_qoi_names
    print(calculated_qoi_names)
    qoi_name = 'MgO.lmps_elastic'
    structures_dict = {
        'ideal':'MgO_Nacl_unit'
    }
    o = LammpsElasticProperties(qoi_name=qoi_name,
                                structures=structures_dict)
    print(o.qoi_name)
    print(o.structures)
    print(o.simulation_definitions)

    o.determine_simulations()
    print(o.simulation_definitions)
