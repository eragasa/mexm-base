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
if __name__ == "__main__":
    qoi_name = "test_qoi_name"
    structures_dict = {
        'ideal':'ideal_structure'
    }
    o = Qoi(qoi_name=qoi_name, structures=structures_dict)
    print(o.qoi_name)
    print(o.structures)
    print(o.simulation_definitions)
