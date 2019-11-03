from mexm import potential
from mexm.potential import Potential

from potentialmap import PotentialMap

def dev__get_potentials():
    print(80*'-')
    print('{:^80}'.format('PotentialMap.get_potentials()'))
    print(80*'-')
    potential_list = PotentialMap.get_potentials()
    print(potential_list)

def dev__get_potential_types():
    print(80*'-')
    print('{:^80}'.format('PotentialMap.get_potentials()'))
    print(80*'-')
    potential_types = PotentialMap.get_potential_types()
    print(potential_types)

if __name__ == "__main__":
    dev__get_potentials()
    dev__get_potential_types()

