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
        outcar(Outcar): initialized as None, object initialized on read()
        contcar(Contcar): initailized as None, object initialized on read()
        oszicar(Ozicar): initialized as None, object initialized on read()
    """

    def __init__(self):
        self.incar = Incar()
        self.poscar = Poscar()
        self.potcar = Potcar()
        self.kpoints = Kpoints()
        self.outcar = None
        self.contcar = None
        self.oszicar = None

    @property
    def total_energy(self):
        return self.outcar.total_energy

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

        if os.path.isfile(oszicar_path):
            self.oszicar = Oszicar()
            self.oszicar.read(path=oszicar_path)

        if os.path.isfile(outcar_path):
            self.outcar = Outcar()
            self.outcar.read(path=outcar_path)

        if os.path.isfile(contcar_path):
            self.contcar = Contcar()
            self.contcar.read(path=contcar_path)
    
    def update_hpc_configuration(self, n_cores, n_nodes):
        pass

