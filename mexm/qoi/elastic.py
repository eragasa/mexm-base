class ElasticPropertyCalculations(Qoi):
    qoi_type = 'base_elastic'
    qois_calculated = ['c11','c12','c13','c22','c33','c44','c55','c66']

    def __init__(self, qoi_name, structures):
        Qoi.__init__(self,
                     qoi_name=qoi_name,
                     structures=structures)

    def determine_simulations(self):
        raise NotImplementedError
