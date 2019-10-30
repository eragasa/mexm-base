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
    'bornmayer': {
        'configuration':{
            'potential_type':'bornmayer',
            'symbols':['Ni', 'Al']}
    },
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
            'pair_type':'bornmayer',
            'density_type':'eamdens_exp',
            'embedding_type':'eamembed_universal'
        }
    },
    'eamembed_universal':{
        'configuration':{
            'potential_type':'eamembed_universal',
            'symbols':['Ni', 'Al']
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

        pair_type = ""
        if 'pair_type' in configuration:
            pair_type = configuration['pair_type']

        density_type = ""
        if 'density_type' in configuration:
            density_type = configuration['density_type']

        embedding_type = ""
        if 'embedding_type' in configuration:
            embedding_type = configuration['embedding_type']

        potential = PotentialManager.get_potential_by_name(
            potential_name = potential_name,
            symbols = symbols,
            pair_type = pair_type,
            density_type = density_type,
            embedding_type = embedding_type
        )

def dev__potential__list_potentials():
    potential_map = PotentialManager.get_potential_map()
    for k, v in potential_map.items():
        format_str = "{:40}{:40}"
        print(format_str.format(k,v['module']))
        print(format_str.format('',v['class']))

if __name__ == "__main__":
    dev__potential__list_potentials()
