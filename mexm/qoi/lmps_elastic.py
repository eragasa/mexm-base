from collections import OrderedDict
from mexm.qoi import ElasticProperties

class LammpsElasticProperties(ElasticProperties):
    qoi_type = 'lmps_elastic'


    def __init__(self,qoi_name,structures):
        assert isinstance(qoi_name,str)

        _qoi_name = qoi_name
        _qoi_type = 'lmps_elastic'

        _structures = OrderedDict()
        if isinstance(structures,str):
            _structures['ideal'] = structures
        elif isinstance(structures,dict):
            _structures['ideal'] = structures['ideal']
        elif isinstance(structures,list):
            _structures['ideal'] = structures[0]
        else:
            msg_err = (
                "structures must be either str, dict, or list"
            )
            raise ValueError(msg_err)

        Qoi.__init__(self, qoi_name=qoi_name, structures=_structures)

    def determine_simulations(self):
        ideal_structure_name = self.structures['ideal']
        ideal_simulation_type = 'lmps_elastic'
        ideal_simulation_name = '{}.{}'.format(ideal_structure_name,
                                               ideal_simulation_type)
        self.add_simulation(sim_id='ideal',
                            simulation_name=ideal_simulation_name,
                            simulation_type=ideal_simulation_type,
                            simulation_structure=ideal_structure_name)

    def calculate_qois(self,simulation_results):
        ideal_sim_name = self.simulation_definitions['ideal']

        for k in ['c11','c12','c13','c22','c33','c44','c55','c66']:
            qoi_name = '{}.{}'.format(ideal_sim_name, k)
            self.qois[qoi_name] = simulation_results[qoi_name]

        c11 = simulation_results['{}.{}'.format(ideal_sim_name,'c11')]
        c12 = simulation_results['{}.{}'.format(ideal_sim_name,'c12')]
        # c13 = simulation_results['{}.{}'.format(_prefix,'c13')]
        # c22 = simulation_results['{}.{}'.format(_prefix,'c22')]
        # c33 = simulation_results['{}.{}'.format(_prefix,'c33')]
        # c44 = simulation_results['{}.{}'.format(_prefix,'c44')]
        # c55 = simulation_results['{}.{}'.format(_prefix,'c55')]
        # c66 = simulation_results['{}.{}'.format(_prefix,'c66')]

        # References:
        # http://homepages.engineering.auckland.ac.nz/~pkel015/SolidMechanicsBooks/Part_I/BookSM_Part_I/06_LinearElasticity/06_Linear_Elasticity_03_Anisotropy.pdf

        bulk = (c11+2*c12)/3
        shear = (c11-c12)/2

        self.qois['{}.bulk_modulus'.format(ideal_sim_name)] = bulk
        self.qois['{}.shear_modulus'.format(ideal_sim_name)] = shear
