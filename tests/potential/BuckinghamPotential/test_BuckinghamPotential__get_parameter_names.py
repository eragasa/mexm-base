import pytest
from collections import OrderedDict
from mexm.potential import BuckinghamPotential

if __name__ == "__main__":
    symbols = ['Mg', 'O']
    parameter_names = BuckinghamPotential.get_parameter_names(
            symbols=symbols,
            hybrid_format=False
    )
    print(parameter_names)
