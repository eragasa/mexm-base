from mexm import potential
from mexm.potential import Potential

class PotentialMap(object):

    def get_potentials():
        potential_list = []

        for p in Potential.__subclasses__():
            potential_list.append(p)
       
        for p in potential_list:

        return potential_list

    def get_potential_types():
        potential_list = PotentialMap.get_potentials()

        potential_types = []
        for potential in potential_list:
            try:
                potential_type = potential.potential_type
                potential_types.append(potential_type)
            except AttributeError as e:
                pass
        return potential_types

potential_list = PotentialMap.get_potentials()
print(potential_list)
potential_types = PotentialMap.get_potential_types()
print(potential_types)

exit()
potential_list = []
for potential in Potential.__subclasses__():
    print(potential,potential.__subclasses__())
    if potential.__subclasses__() != []:
       potential_list.append(potential)

    for sub_potential in potential.__subclasses__():
        if potential.__subclasses__() != []:
           potential_list.append(potential)

exit()

for i in dir(potential):
    print(i," ",type(getattr(potential,i)))
    #print(getattr(potential,i))
    #print(isinstance(getattr(potential,i),Potential))
