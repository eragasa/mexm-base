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
    o = LammpsElasticProperties(qoi_name=qoi_name,
                                structures=structures_dict)
    o.determine_simulations()
    assert o.qoi_name == 'MgO.lmps_elastic'
    assert o.structures == structures_dict
    assert o.simulation_definitions == {
        'ideal':{
            'simulation_name':'MgO_NaCl_unit.lmps_elastic',
            'simulation_type':'lmps_elastic',
            'simulation_structure':'MgO_NaCl_unit',
            'bulk_structure':None
        }
    }

def test__LammpsElasticProperties__calculate_qois():
    assert False
if __name__ == "__main__":
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
