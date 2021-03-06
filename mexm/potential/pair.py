from collections import OrderedDict

from mexm.potential import MEXM_1BODY_FORMAT
from mexm.potential import MEXM_2BODY_FORMAT

from mexm.potential import Potential
from mexm.potential import get_symbol_pairs

class PairPotential(Potential):
    def __init__(self,symbols,potential_type,is_charge):
        Potential.__init__(self,
                symbols=symbols,
                potential_type=potential_type,
                is_charge=is_charge)
        self.pair_evaluations = None
        #self.pair_potential_parameters = None
        #self.symbol_pairs = None

    def _initialize_parameter_names(self,symbols=None):
        if symbols is None:
            symbols = self.symbols

        self.symbol_pairs = list(get_symbol_pairs(symbols))

        # initialize attribute to populate
        self.parameter_names = []
        if self.is_charge:
            for s in self.symbols:
                parameter_name = MEXM_1BODY_FORMAT.format(s=s, p='chrg')
                self.parameter_names.append(parameter_name)

        for sp in self.symbol_pairs:
            for p in self.pair_potential_parameters:
                parameter_name = MEXM_2BODY_FORMAT.format(
                    s1=sp[0],
                    s2=sp[2],
                    p=p
                )
                self.parameter_names.append(parameter_name)

        return self.parameter_names

    def _initialize_parameters(self):
        self.parameters = OrderedDict()
        for v in self.parameter_names:
            self.parameters[v] = None
