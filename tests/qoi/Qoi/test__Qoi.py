from mexm.qoi import Qoi

def test__Qoi__init():
    qoi_name = "test_qoi_name"
    structures_dict = {
        'ideal':'ideal_structure'
    }
    o = Qoi(qoi_name=qoi_name, structures=structures_dict)

    assert o.qoi_name == qoi_name
    assert o.structures == structures_dict
    assert o.simulation_definitions == {}

def test__Qoi__add_simulation__no_bulk_structure():
    qoi_name = "test_qoi_name"
    structures_dict = {
        'ideal':'ideal_structure'
    }
    o = Qoi(qoi_name=qoi_name, structures=structures_dict)

    kwargs = {
        'sim_id':'test_sim_id',
        'simulation_name':'test_simulation_name',
        'simulation_type':'simulation_type',
        'simulation_structure':'test_simulation_structure_name',
    }
    o.add_simulation(**kwargs)
    assert o.simulation_definitions == {
        'test_sim_id': {
            'simulation_name': 'test_simulation_name',
            'simulation_type': 'simulation_type',
            'simulation_structure': 'test_simulation_structure_name',
            'bulk_structure': None}}

def test__Qoi__add_simulation__w_bulk_structure():
    qoi_name = "test_qoi_name"
    structures_dict = {
        'ideal':'ideal_structure'
    }
    o = Qoi(qoi_name=qoi_name, structures=structures_dict)

    kwargs = {
        'sim_id':'test_sim_id',
        'simulation_name':'test_simulation_name',
        'simulation_type':'simulation_type',
        'simulation_structure':'test_simulation_structure_name',
        'bulk_structure':'test_bulk_structure_name'
    }
    o.add_simulation(**kwargs)
    assert o.simulation_definitions == {
        'test_sim_id': {
            'simulation_name': 'test_simulation_name',
            'simulation_type': 'simulation_type',
            'simulation_structure': 'test_simulation_structure_name',
            'bulk_structure': 'test_bulk_structure_name'}}


if __name__ == "__main__":
    qoi_name = "test_qoi_name"
    structures_dict = {
        'ideal':'ideal_structure'
    }
    o = Qoi(qoi_name=qoi_name, structures=structures_dict)
    print(o.qoi_name)
    print(o.structures)
    print(o.simulation_definitions)

    kwargs = {
        'sim_id':'test_sim_id',
        'simulation_name':'test_simulation_name',
        'simulation_type':'simulation_type',
        'simulation_structure':'test_simulation_structure_name',
    }
    o.add_simulation(**kwargs)
    print(o.simulation_definitions)
