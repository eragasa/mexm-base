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
print(obj.incar.to_string())
assert isinstance(obj.poscar, Poscar)
assert isinstance(obj.kpoints, Kpoints)
assert isinstance(obj.potcar, Potcar)

# check to see if the types of the vasp outfiles were done correctly
assert isinstance(obj.outcar, Outcar)
assert isinstance(obj.oszicar, Oszicar)
print('electric_scf')
for scf_info in obj.oszicar.electric_scf:
    print(scf_info)
print('ionic_relaxation')
for ionic_info in obj.oszicar.ionic_relaxation:
    print(ionic_info)
print('n_ionic:{}'.format(obj.oszicar.n_ionic))
print(obj.oszicar.n_scf)
