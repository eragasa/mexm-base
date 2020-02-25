from mexm.simulation.base import Simulation
from mexm.simulation.base import AtomicSimulation

from mexm.simulation.lammps import LammpsSimulation
from mexm.simulation.gulp import GulpSimulation
from mexm.simulation.phonts import PhontsSimulation
from mexm.simulation.vasp import VaspSimulation

from mexm.simulation.min_all import StructuralMinimization
from mexm.simulation.lmps_min_all import LammpsStructuralMinimization
class GulpStructuralMinimization(GulpSimulation, StructuralMinimization): pass
class VaspStructuralMinimization(VaspSimulation, StructuralMinimization): pass

class StaticCalculation(Simulation): pass
from mexm.simulation.lmps_min_none import LammpsStaticCalculation
class GulpStaticCalculation(GulpSimulation, StaticCalculation): pass
class VaspStaticCalculation(VaspSimulation, StaticCalculation): pass

class PositionMinimization(Simulation): pass
from mexm.simulation.lmps_min_pos import LammpsPositionMinimization
class GulpPositionMinimization(GulpSimulation, PositionMinimization): pass
class VaspPositionMinimization(VaspSimulation, PositionMinimization): pass

class PhononCalculation(Simulation): pass
class GulpPhononCalculation(GulpSimulation, PhononCalculation): pass
class VaspPhononCalculation(VaspSimulation, PhononCalculation): pass

class NptSimulation(Simulation): pass
from mexm.simulation.lmps_npt import LammpsNptSimulation

class NvtSimulation(Simulation): pass
from mexm.simulation.lmps_nvt import LammpsNvtSimulation

class SimulationFactory():
    factories = dict(
        {k.name:k in LammpsSimulation.__subclasses__}.items(),
        {k.name:k in GulpSimulation.__subclasses__}.items(),
        {k.name:k in PhontsSimulation.__subclasses__}.items(),
        {k.name:k in Vasp.__subclasses__}.items()
    )

from mexm.simulation.manager import SimulationManager
from mexm.simulation.manager import SerialSimulationManager
from mexm.simulation.manager import MpiSimulationManager
