from mexm.simulation import AtomicSimulation
from mexm.io.vasp import (Incar, Poscar, Potcar, Kpoints)

class VaspSimulation(AtomicSimulation):
    def __init__(self):
        self.incar = Incar()
        self.poscar = Poscar()
        self.potcar = Potcar()
        self.kpoints = Kpoints()
        self.outcar = Outcar()
        self.contcar = Poscar()
        self.oszicar = Oszicar()

    
