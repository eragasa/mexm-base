simulation_path = 'resource'

from mexm.io.vasp import Poscar
from mexm.io.vasp import Incar
from mexm.io.vasp import Kpoints
from mexm.io.vasp import Potcar

from mexm.io.vasp import Outcar
from mexm.io.vasp import Oszicar
from mexm.simulation import VaspSimulation

obj = VaspSimulation()
obj.read(simulation_path=simulation_path)

# check to see if the types of the input files were done correctly
assert isinstance(obj.incar, Incar)
assert isinstance(obj.poscar, Poscar)
assert isinstance(obj.kpoints, Kpoints)
assert isinstance(obj.potcar, Potcar)

# check to see if the types of the vasp outfiles were done correctly
assert isinstance(obj.outcar, Outcar)
assert isinstance(obj.oszicar, Oszicar)
print(obj.oszicar.n_scf)
print(obj.oszicar.n_ionic)
print(obj.oszicar.electric_scf)
print(obj.oszicar.ionic_relaxation)