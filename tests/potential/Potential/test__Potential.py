from collections import OrderedDict
from mexm.potential import get_symbol_pairs
from mexm.potential import get_pair_parameter_names
from mexm.potential import Potential

class PotentialTester(Potential):

    pair_parameter_names = ['A', 'B']

    def _init_parameter_names(self):
        self.symbol_pairs = get_symbol_pairs(self.symbols)
        self.parameter_names = get_pair_parameter_names(
                symbols = self.symbols,
                pair_parameter_names = PotentialTester.pair_parameter_names)

    def _init_parameters(self):
        self.parameters = OrderedDict(
            [(k,None) for k in self.parameter_names]
        )


def test____init____no_args():
    symbols = ['Ni']
    potential = PotentialTester(symbols=symbols)

    assert potential.potential_type == None
    assert potential.is_charge == False


def test____init____with_args():
    symbols = ['Ni']
    potential_type = 'potential_type'
    is_charge=False
    expected_potential_type = potential_type
    expected_is_charge = is_charge
    expected_parameter_names = ['NiNi_A', 'NiNi_B']
    potential = PotentialTester(symbols=symbols, potential_type=potential_type)
    assert potential.potential_type == expected_potential_type
    assert potential.is_charge == expected_is_charge
    assert potential.parameter_names == expected_parameter_names

def test___get_mass():

    symbols = ['Ni']
    potential_type = 'potential_type'
    is_charge=False
    expected_potential_type = potential_type
    expected_is_charge = is_charge
    expected_parameter_names = ['NiNi_A', 'NiNi_B']
    potential = PotentialTester(symbols=symbols, potential_type=potential_type)

    for s in symbols:
        assert isinstance(potential._get_mass(symbol=s), float)

def test___get_name():

    symbols = ['Ni']
    potential_type = 'potential_type'
    is_charge=False
    expected_potential_type = potential_type
    expected_is_charge = is_charge
    expected_parameter_names = ['NiNi_A', 'NiNi_B']
    potential = PotentialTester(symbols=symbols, potential_type=potential_type)

    for s in symbols:
        assert isinstance(potential._get_name(symbol=s), str)

def dev___get_mass():
    symbols = ['Ni']
    potential_type = 'potential_type'
    is_charge=False
    expected_potential_type = potential_type
    expected_is_charge = is_charge
    expected_parameter_names = ['NiNi_A', 'NiNi_B']
    potential = PotentialTester(symbols=symbols, potential_type=potential_type)

    for s in symbols:
        print("potential._get_mass({})={}".format(
            s,
            potential._get_mass(symbol=s)))

def dev___get_name():
    symbols = ['Ni']
    potential_type = 'potential_type'
    is_charge=False
    expected_potential_type = potential_type
    expected_is_charge = is_charge
    expected_parameter_names = ['NiNi_A', 'NiNi_B']
    potential = PotentialTester(symbols=symbols, potential_type=potential_type)

    for s in symbols:
        print("potential.__get_name({})={}".format(
            s,
            potential._get_name(symbol=s), str
        ))
if __name__ == "__main__":
    dev___get_mass()
    dev___get_name()
