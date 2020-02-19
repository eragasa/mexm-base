import numpy as np
from mexm.structure import SimulationCell

class VaspPoscarError(Exception):
    def __init__(self,*args,**kwargs):
        """Error class for reading/writing VASP POSCAR IO issues """
        Exception.__init__(self,*args,**kwargs)

class Poscar(SimulationCell):
    """ POSCAR structure file for VASP

        Args:
            obj_cell (pypospack.crystal.SimulationCell):

        Attributes:
            path (str): path (either to be written to or to write from)
            comment (str): comment used in the first line of the POSCAR file
    """

    def __init__(self):
        super().__init__()
        self.path = 'POSCAR'
        self.comment = 'Automatically generated by pypospack'

    def get_magmom_tag(self):
        magmom = [k.magmom for k in self.atomic_basis]

        str_magmom = ""

        current_magmom = None
        n_magmom = 0
        for m in magmom:
            if current_magmom == m:
                n_magmom += 1
            else:
                if current_magmom == None:
                    pass
                else:
                    str_magmom += "{}*{} ".format(n_magmom,current_magmom)
                current_magmom = m
                n_magmom = 1
        str_magmom += "{}*{} ".format(n_magmom,current_magmom)

        str_magmom = str_magmom.strip()
        return str_magmom

    def read(self, path=None):
        """ read the POSCAR file

        Args:
            path (str): the file name of the POSCAR file
        """
        if path is not None:
            self.path = path

        try:
            f = open(self.path, 'r')
        except FileNotFoundError as e:
            raise
        self.comment = f.readline().strip()

        # read lattice parameter
        try:
            line = f.readline()
            self.a0 = float(line)
        except ValueError as e:
            msg = "Cannot read the lattice parameter from the POSCAR file\n"
            raise ValueError(msg)

        h_matrix = np.zeros(shape=[3,3])
        for i in range(3):
            h_col = f.readline().strip().split()
            h_col = np.array([float(val) for val in h_col])
            h_matrix[:,i] = h_col
        self.H = h_matrix.copy()

        # read symbols
        symbols = f.readline().strip().split()

        # number of atoms per symbol
        n_atoms_per_symbol = {}
        line = f.readline().strip().split()
        for i,n in enumerate(line):
            s = symbols[i]
            n_atoms_per_symbol[s] = int(n)

        # read in coordinate type
        line = f.readline()
        coordinate_style = line[0].upper()
        if coordinate_style == "D":
            self.coordinate_style = "Direct"
        elif coordinate_style == "C":
            self.coordinate_style = "Cartesian"
        else:
            msg = "unable to determine the coordinate style {}".format(line)
            raise VaspPoscarError(msg)

        # read in atomic positions
        for s in symbols:
            n_atoms = n_atoms_per_symbol[s]
            for i_atom in range(n_atoms):
                line = f.readline().strip().split()
                position = [float(line[i]) for i in range(3)]
                try:
                    self.add_atom(s,position)
                except:
                    raise

    def write(self, path=None):
        """ write poscar file
        
        Arguments:
            path(str): the path to write the POSCAR file too
        """
        if path is None:
            path = self.path
        self.path = path

        str_poscar  = self.comment + "\n"
        str_poscar += "{:10.6}\n".format(self.a0)

        # string for h-matrix
        for i in range(3):
            h_row_template = "{:10.6f} {:10.6f} {:10.6f}\n"
            str_poscar += h_row_template.format(self.H[0,i],
                                                self.H[1,i],
                                                self.H[2,i])

        sym_list = self.symbols
        str_atomlist = ""
        str_atomnum  = ""
        for sym in sym_list:
            nAtoms = self.get_number_of_atoms(sym)
            str_atomlist   += " " + sym
            str_atomnum    += " " + str(nAtoms)
        str_atomlist   += "\n"
        str_atomnum    += "\n"

        str_poscar += str_atomlist
        str_poscar += str_atomnum
        str_poscar += "Direct\n"

        for symbol in self.symbols:
            for i, atom in enumerate(self.atomic_basis):
                if symbol == atom.symbol:
                    pos_template = "{:10.6f} {:10.6f} {:10.6f}\n"
                    str_position = pos_template.format(atom.position[0],
                                                       atom.position[1],
                                                       atom.position[2])
                    str_poscar += str_position

        f = open(self.path, 'w')
        f.write(str_poscar)
        f.close()
