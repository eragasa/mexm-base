
class Oszicar():
    str_scf_step = "N       E                     dE             d eps       ncg     rms          rms(c)"

    """ class to read OSZICARs from VASP

    Properties:
        n_scf (int): total_number of self-consistent steps
        n_ionic (int): total number of ionic relaxation
        electric_scf (list of dict): convergence info for SCF calculations
        ionic_relaxation (list of dict): convergernce info for ionic relaxation steps
    """
    def __init__(self):
        self.path_ = None
        self.n_scf = None
        self.n_ionic = None
        self.electric_scf = None
        self.ionic_relaxation = None

    @property
    def path(self):
        return self.path_

    @path.setter
    def path(self, path):
        if not isinstance(path, str):
            msg = 'path must be a string'
            raise TypeError(msg)

        self.path_ = path

    def write(self, path):
        raise NotImplementedError

    def read(self, path):
        """ read an OSZICAR file

        Args:
           path (str): path to the OSZICAR file
        """
        
        self.path = path

        with open(self.path, 'r') as f:
            lines = [k.strip() for k in f.readlines()]

        n_lines = len(lines)

        n_scf = 0
        electric_scf = []

        n_ionic = 0
        ionic_relaxation = []

        i_line = 0
        while i_line < n_lines:
            if lines[i_line] == Oszicar.str_scf_step:
                electric_scf.append({})
                n_scf += 1
            elif lines[i_line].startswith('DAV:'):
                tokens = [k.strip() for k in lines[i_line].split()]
                electric_scf[n_scf-1]['N'] = int(tokens[1])
                electric_scf[n_scf-1]['E'] = float(tokens[2])
                electric_scf[n_scf-1]['dE'] = float(tokens[3])
                electric_scf[n_scf-1]['d_eps'] = float(tokens[4])
                electric_scf[n_scf-1]['ncg'] = int(tokens[5])
                electric_scf[n_scf-1]['rms'] = float(tokens[6])
                try:
                    electric_scf[n_scf-1]['rms_c'] = float(tokens[7])
                except IndexError:
                    electric_scf[n_scf-1]['rms_c'] = None
            else:
                tokens = [k.strip() for k in lines[i_line].split()]
                ionic_relaxation.append({
                    'N':float(tokens[0]),
                    'F':float(tokens[2]),
                    'E0':float(tokens[4]),
                    'dE0':float(tokens[7][1:])
                })
            i_line += 1

        # put into attribute, eventually change to properties        
        self.n_scf = n_scf
        self.n_ionic = n_ionic
        self.electric_scf = electric_scf
        self.ionic_relaxation = ionic_relaxation
            