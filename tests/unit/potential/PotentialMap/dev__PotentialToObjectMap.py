from mexm import potential
from mexm.potential import Potential

def get_base_potentials():
    base_potentials = [p for p in Potential.__subclasses__()]
    return base_potentials

def get_potentials():
    potentials = []
    for base_potential in get_base_potentials():
        potential

def dev__get_base_potentials():
    base_potentials = get_base_potentials()
    
    print(80*'-')
    print('base_potentials')
    print(80*'-')
    for p in base_potentials:
        print(p)


potential_list = []
for p in Potential.__subclasses__():
    print(p)
    potential_list.append(p)

    for sub_p in p.__subclasses__():
        print(sub_p)
        potential_list.append(sub_p)

print('potential_list')
print(potential_list)

if __name__ == "__main__":
    dev__get_base_potentials()
