class SimulationState(ABC):
    name = 'defaultstate'  # must be overridden

    @abstractclassmethod
    cls check_conditions(cls, simulation: Simulation) -> bool:
        raise NotImplementedError

class SimulationStates(ABC):
    # the dictionary has to be ordered to ensure the simulations state
    # gets checked correctly
    factories = OrderedDict()  
    
    @abstractclassmethod
    cls on_update(cls, simulation: Simulation) -> str: pass:

        state = None # initialize the return variable
        for k, v in cls.factories.items(k:
            if k.check_conditions():
                state = k
            else:
                break
        return state
