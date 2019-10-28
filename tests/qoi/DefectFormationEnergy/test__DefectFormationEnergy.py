from mexm.qoi import DefectFormationEnergy

def test__DefectFormationEnergy__qoi_type():
    DefectFormationEnergy.qoi_type == 'base_defect'

def test__DefectFormationEnergy__calculated_qoi_names():
    DefectFormationEnergy.calculated_qoi_names = ['E_formation']

def test__DefectFormationEnergy__is_base_class():
    DefectFormationEnergy.is_base_class = True

def test__DefectFormationEnergy__simulation_types():
    DefectFormationEnergy.ideal_simulation_type == 'min_all'
    DefectFormationEnergy.defect_simulation_type == 'min_pos'

def dev__DefectFormationEnergy____init__():
    kwargs = {
        'qoi_name':'test_qoi_name',
        'structures':{
            'ideal':'MgO_NaCl_unit',
            'defect':'MgO_NaCl_fr'
        }
    }
    expected_simulation_definitions = {
        'ideal': {
            'simulation_name': 'MgO_NaCl_unit.min_all',
            'simulation_type': 'min_all',
            'simulation_structure': 'MgO_NaCl_unit',
            'bulk_structure': None},
        'defect': {
            'simulation_name': 'MgO_NaCl_fr.min_pos',
            'simulation_type': 'min_pos',
            'simulation_structure': 'MgO_NaCl_fr',
            'bulk_structure': 'MgO_NaCl_unit'}
    }
    o = DefectFormationEnergy(**kwargs)

def dev__DefectFormationEnergy__determine_simulations():
    kwargs = {
        'qoi_name':'test_qoi_name',
        'structures':{
            'ideal':'MgO_NaCl_unit',
            'defect':'MgO_NaCl_fr'
        }
    }
    o = DefectFormationEnergy(**kwargs)
    o.determine_simulations()

    for sim_k, sim_info in o.simulation_definitions.items():
        print(sim_k)
        for k, v in sim_info.items():
            if v is not None:
                line_fmt = '\t{:25}{:25}'
                print(line_fmt.format(k,v))

def dev__DefectFormationEnergy__determine_simulations():
    kwargs = {
        'qoi_name':'test_qoi_name',
        'structures':{
            'ideal':'MgO_NaCl_unit',
            'defect':'MgO_NaCl_fr'
        }
    }
    expected_simulation_definitions = {
        'ideal': {
            'simulation_name': 'MgO_NaCl_unit.min_all',
            'simulation_type': 'min_all',
            'simulation_structure': 'MgO_NaCl_unit',
            'bulk_structure': None},
        'defect': {
            'simulation_name': 'MgO_NaCl_fr.min_pos',
            'simulation_type': 'min_pos',
            'simulation_structure': 'MgO_NaCl_fr',
            'bulk_structure': 'MgO_NaCl_unit'}
    }
    o = DefectFormationEnergy(**kwargs)
    for sim_k, sim_info in expected_simulation_definitions.items():
        for k, v, in sim_info.items():
            assert o.simulation_definitions[sim_k][k] == v
if __name__ == "__main__":
    dev__DefectFormationEnergy____init__()
    dev__DefectFormationEnergy__determine_simulations()
