import importlib

pair_potentials = {
    'buckingham':{'module':'mexm.potential', 'class':'BuckinghamPotential'},
    'morse':{'module':'mexm.potential', 'class':'MorsePotential'},
    'bornmayer':{'module':'mexm.potential', 'class':'BornMayerPotential'},
    'lj':{'module':'mexm.potential', 'class':'LennardJonesPotential'},
    'general_lj':{'module':'mexm.potential', 'class':'GeneralizedLennardJonesPotential'}
}

threebody_potentials = {
    'sw':{
        'module':'pypospack.potential',
        'class':'TersoffPotential'},
    'tersoff':{
        'module':'pypospack.potential',
        'class':'StillingerWeberPotential'}
}

eam_density_functions = {
    'eam_dens_exp':{
        'module':'pypospack.potential',
        'class':'ExponentialDensityFunction'},
    'eam_dens_mishin2004':{
        'module':'pypospack.potential',
        'class':'Mishin2004DensityFunction'}
    }

eam_embedding_functions = {
        'eam_embed_universal':{
            'module':'pypospack.potential',
            'class':'UniversalEmbeddingFunction'},
        'eam_embed_bjs':{
            'module':'pypospack.potential',
            'class':'BjsEmbeddingFunction'},
        'eam_embed_fs':{
            'module':'pypospack.potential',
            'class':'FinnisSinclairEmbeddingFunction'},
        'eam_embed_eos_rose':{
            'module':'pypospack.potential',
            'class':'RoseEquationOfStateEmbeddingFunction'},
        'eam_embed_eos_zopemishin':{
            'module':'pypospack.potential',
            'class':'ZopeMishinEosEmbeddingFunction'}
        }

def get_potential(module_name, class_name, symbols):
    module_ = importlib.import_module(module_name)
    class_ = getattr(module_, class_name)
    return class_(symbols=symbols)

def get_pair_potential(name,symbols):
    module_name = pair_potentials[name]['module']
    class_name = pair_potentials[name]['class']

    return get_potential(module_name=module_name, class_name=class_name, symbols=symbols)

def get_3body_potential(name,symbols):
    module_name = threebody_potentials[name]['module']
    class_name = threebody_potentials[name]['class']
    return get_potential(module_name=module_name, class_name=class_name, symbols=symbols)

def get_eam_density_function(name,symbols):
    module_name = eam_density_functions[name]['module']
    class_name = eam_density_functions[name]['class']
    return get_potential(module_name=module_name, class_name=class_name, symbols=symbols)

def get_eam_embedding_function(name,symbols):
    module_name = eam_embedding_functions[name]['module']
    class_name = eam_embedding_functions[name]['class']
    return get_potential(module_name=module_name, class_name=class_name, symbols=symbols)
