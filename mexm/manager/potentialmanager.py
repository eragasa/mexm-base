import importlib
from collections import OrderedDict
from mexm.potential import PotentialConfiguration
from mexm.potential import Potential


class PotentialManager(object):

    @staticmethod
    def get_potential_map():
        potential_map = OrderedDict()
        for k in PotentialManager.get_potential_types():
            if not k.is_base_potential:
                potential_map[k.potential_type] = {
                    'module': k.__module__,
                    'class': k.__name__
                }
        return potential_map

    @staticmethod
    def get_potential(module_name, class_name, symbols):
        module_ = importlib.import_module(module_name)
        class_ = getattr(module_, class_name)
        return class_(symbols=symbols)

    @staticmethod
    def get_potential_by_name(potential_name, symbols):
        potential_map = PotentialManager.get_potential_map()
        module_name = potential_map[potential_name]['module']
        class_name = potential_map[potential_name]['class']
        return PotentialManager.get_potential(module_name, class_name, symbols)

    @staticmethod
    def get_potential_types():

        potential_list = []
        for p in Potential.__subclasses__():
            potential_list.append(p)

        n_potentials = -1
        while (len(potential_list) > n_potentials):
            n_potentials = len(potential_list)
            print(n_potentials)
            for p in potential_list:
                potential_list += [k for k in p.__subclasses__() if k not in potential_list]
        return potential_list

    @staticmethod
    def get_potential_names():
        potential_list = PotentialManager.get_potential_types()

        potential_types = []
        for potential in potential_list:
            try:
                potential_type = potential.potential_type
                potential_types.append(potential_type)
            except AttributeError as e:
                pass
        return potential_types

PotentialtoClassMap = PotentialManager.get_potential_map()
