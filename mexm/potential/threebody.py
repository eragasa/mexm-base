from collections import OrderedDict
from mexm.potential import Potential

class ThreeBodyPotential(Potential):

    def _initialize_parameter_names(self):
        # TODO: This is only written for a single element potential
        self._initialize_2body_parameter_names()
        self._initialize_3body_parameter_names()
        
    def _add_parameter_names(self,el1,el2,el3):
        s = "{}{}{}".format(el1,el2,el3)

        self.parameter_names = []
        for p in self.threebody_parameter_names:
            self.parameter_names.append('{}__{}'.format(s,p))

    def _init_parameters(self):
        self.parameters = OrderedDict()
        for p in self.parameter_names:
            self.parameters[p] = None
