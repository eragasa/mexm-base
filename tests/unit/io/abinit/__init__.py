
def convert_angstrom_to_bohr(d):
    """
    Args:
        d (float): length unit in Angstroms
    """

    d_Bohr = d / 0.5291772108

    return d_Bohr

def convert_bohr_to_angstrom(d):
    """
    Args:
        d (float): length unit in Angstroms
    """

    d_Angs = d * 0.5291772108

    return d_Angs 


class AbinitInput(): 

    def __init__(self):
        self.tag_values = {}

    @property
    def acell(self):
        try:
            return self.tag_values['acell']
        except KeyError:
            return None

    @acell.setter
    def acell(self, a0):
        if not isinstance(a0, float):
            msg = "acell must be a float type"
            raise TypeError(msg)
        if a0 <= 0.:
            msg = "acell must be greater than zero"
            raise ValueError(msg)

        self.tag_values['acell'] = a0

    @property
    def prim(self):
        return self.tag_values['prim']

