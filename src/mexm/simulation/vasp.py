import os

from mexm.simulation import AtomicSimulation
from mexm.io.vasp import Incar
from mexm.io.vasp import Poscar
from mexm.io.vasp import Potcar
from mexm.io.vasp import Kpoints
from mexm.io.vasp import Outcar
from mexm.io.vasp import Oszicar
from mexm.io.vasp import Contcar

class VaspSimulation():
    """

    Attributes:
        incar(Incar)
        poscar(Poscar)
        kpoints(Kpoints)
        outcar(Outcar)
        contcar(Contcar)
        oszicar(Ozicar)
    """

    def __init__(self):
        self.incar = Incar()
        self.poscar = Poscar()
        self.potcar = Potcar()
        self.kpoints = Kpoints()
        self.outcar = Outcar()
        self.contcar = Contcar()
        self.oszicar = Oszicar()

    def write(self, simulation_path):
        self.path = simulation_path

        poscar_path = os.path.join(simulation_path, 'POSCAR')
        potcar_path = os.path.join(simulation_path, 'POTCAR')
        incar_path = os.path.join(simulation_path, 'INCAR')
        kpoints_path = os.path.join(simulation_path, 'KPOINTS')

        self.poscar.write(path=poscar_path)
        self.potcar.symbols = self.poscar.symbols
        self.potcar.write(path=potcar_path)
        self.incar.write(path=incar_path)
        self.kpoints.write(path=kpoints_path)

    def read(self, simulation_path):
        self.path = simulation_path

        # these files are the input files
        poscar_path = os.path.join(simulation_path, 'POSCAR')
        potcar_path = os.path.join(simulation_path, 'POTCAR')
        incar_path = os.path.join(simulation_path, 'INCAR')
        kpoints_path = os.path.join(simulation_path, 'KPOINTS')

        self.poscar.read(path=poscar_path)
        self.potcar.read(path=potcar_path)
        self.incar.read(path=incar_path)
        self.kpoints.read(path=kpoints_path)


        # these files are the output files
        oszicar_path = os.path.join(simulation_path, 'OSZICAR')
        outcar_path = os.path.join(simulation_path, 'OUTCAR')
        contcar_path = os.path.join(simulation_path, 'CONTCAR')

        try:
            self.oszicar.read(path=oszicar_path)
        except FileNotFoundError:
            pass

        try:
            self.outcar.read(path=outcar_path)
        except FileNotFoundError:
            pass

        try:
            self.contcar.read(path=contcar_path)
        except FileNotFoundError:
            pass
    
    def update_hpc_configuration(self, n_cores, n_nodes):
        pass

