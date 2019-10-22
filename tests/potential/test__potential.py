import pytest
from mexm.potential.lewiscatlow1985 import LewisCatlow1985
from mexm.manager import PotentialManager

from mexm.potential import BuckinghamPotential
buckingham_lewiscatlow1985_buck_MgO ={
    'potential_type':'buckingham',
    'symbols':['Mg','O'],
    'parameters':None
}
buckingham_lewiscatlow1985_buck_MgO['parameters'] = {}
for k in BuckinghamPotential.get_parameter_names(
    symbols = buckingham_lewiscatlow1985_buck_MgO['symbols']
):
    try:
        buckingham_lewiscatlow1985_buck_MgO['parameters'][k] = LewisCatlow1985['parameters'][k]
    except KeyError as e:
        buckingham_lewiscatlow1985_buck_MgO['parameters'][k] = 12.0

from mexm.potential import StillingerWeberPotential

potential_configurations = {
    'buckingham': {
        'configuration':buckingham_lewiscatlow1985_buck_MgO,
        'expected':{}
    },
    'stillingerweber':{
        'configuration':{
            'potential_type':'stillingerweber',
            'symbols':['Si'],
            'parameters':{}
        }
    },
    'eamdens_exp':{
        'configuration':{
            'potential_type':'eamdens_exp',
            'symbols':['Ni','Al']
        }
    },
    'eam':{
        'configuration':
        {
            'potential_type':'eam',
            'symbols':['Ni', 'Al'],
            'func_pair':'bornmayer',
            'func_density':'eamdens_exp',
            'func_embedding':'eamembed_bjs'
        }
    }
}

#@pytest.parameterize(
#    ",".join([k for k in potential_configurations.keys()],
#    [(v) for v in potential_configurations.values()])
#)
def test__potential():
    potential_map = PotentialManager.get_potential_map()
    for k, v in potential_map.items():
        potential_name = k
        configuration = potential_configurations[k]['configuration']
        symbols = configuration['symbols']

        try:
            func_pair = configuration['func_pair']
        except KeyError:
            func_pair = None

        try:
            func_density = configuration['func_density']
        except KeyError:
            func_density =none

        try:
            func_embedding = configuration['func_embedding']
        except KeyError:
            func_embedding = None

        potential = PotentialManager.get_potential_by_name(
            potential_name = potential_name,
            symbols = symbols,
            func_pair = func_pair,
            func_density = func_density,
            func_embedding = func_embedding
        )

def dev__potential__list_potentials():
    potential_map = PotentialManager.get_potential_map()
    for k, v in potential_map.items():
        format_str = "{:40}{:40}"
        print(format_str.format(k,v['module']))
        print(format_str.format('',v['class']))

if __name__ == "__main__":
    dev__potential__list_potentials()
