from mexm.crystal import SimulationCell

class VaspPoscarError(Exception):
    def __init__(self,*args,**kwargs):
        """Error class for reading/writing VASP POSCAR IO issues """
        Exception.__init__(self,*args,**kwargs)

class Poscar(SimulationCell):
    """ POSCAR structure file for VASP

        Args:
            obj_cell (pypospack.crystal.SimulationCell):

        Attributes:
            filename (str): filename (either to be written to or to write from)
            comment (str): comment used in the first line of the POSCAR file
    """

    def __init__(self,obj_cell=None):
        SimulationCell.__init__(self,obj_cell)
        self.filename = 'POSCAR'
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

    def read(self, filename=None):
        """ read the POSCAR file

        Args:
            filename (str): the file name of the POSCAR file
        """
        if filename is not None:
            self.filename = filename

        try:
            f = open(self.filename, 'r')
        except FileNotFoundError as e:
            str_out = "\n".join(
                [
                "cwd={}".format(os.getcwd()),
                "filename={}".format(self.filename)
                ])
            raise
        # read structure comment
        self.comment = f.readline().strip()

        # read lattice parameter
        try:
            line = f.readline()
            self.a0 = float(line)
        except ValueError as e:
            msg_err = "Cannot read the lattice parameter from the POSCAR file\n"
            msg_err += "filename:{}\n".format(self.filename)
            msg_err += "line({}):\'{}\'".format(
                str(type(line)),
                line)
            print(msg_err)
            raise ValueError(line)

        h_matrix = np.zeros(shape=[3,3])
        for i in range(3):
            h_row = f.readline().strip().split()
            h_row = np.array([float(val) for val in h_row])
            h_matrix[i,:] = h_row
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
    def write(self, filename=None):
        """ write poscar file """
        if filename is None:
            filename = self.filename
        self.filename = filename

        str_poscar  = self.comment + "\n"
        str_poscar += "{:10.6}\n".format(self.a0)

        # string for h-matrix
        for i in range(3):
            h_row_template = "{:10.6f} {:10.6f} {:10.6f}\n"
            str_poscar += h_row_template.format(self.H[i,0],
                                                self.H[i,1],
                                                self.H[i,2])

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

        f = open(self.filename, 'w')
        f.write(str_poscar)
        f.close()