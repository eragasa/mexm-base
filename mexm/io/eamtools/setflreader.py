from mexm.io.eamtools import EamSetflFile

class SetflReader(EamSetflFile):
    """Reader for setfl formatted EAM files.

    Args:
        path (str): Path to the setfl file.
    """

    def __init__(self, path=None):
        assert any([
            isinstance(path, str),
            path is None
        ])

        EamSetflFile.__init__(self)
        self.path = path

    def read(self, path=None):
        if path is not None:
            self.path = path
        path_ = self.path

        with open(path_, "r") as f:
            lines = f.readlines()

        self.comments_ = [lines[i].strip() for i in range(3)]

        symbol_info = lines[3].split()
        self.N_symbols = int(symbol_info[0])
        self.symbols = [int(k) for k in symbol_info[1:]]
        self.symbol_pairs = SetflReader.get_symbol_pairs(self.symbols)

        # cutoff info
        cutoff_info = lines[4].split()
        self.N_rho = int(cutoff_info[0])
        self.d_rho = float(cutoff_info[1])
        self.N_r = int(cutoff_info[2])
        self.d_r = int(cutoff_info[3])
        self.r_cutoff = int(cutoff_info[4])

    @staticmethod
    def get_symbol_pairs(symbols):
        assert isinstance(symbols, list)

        pairs = []
        for i1, s1 in enumerate(symbols):
            for i2, s2 in enumerate(symbols):
                if i <= j:
                    pairs.append("{}{}".format(s1, s2))
        return tuple(symbols)

    @property
    def elements(self):
        """Elemental symbols specified in the file.

        Returns:
            tuple of str
        """
        return self._elements_
        #return tuple(self._lines[3].split()[1:])

    @elements.setter
    def elements(self, elements):
        self.elements_ = elements

    @property
    def element_pairs(self):
        """Elemental symbol pairs specified in the file.

        Returns:
            tuple of str
        """
        pairs = []
        for i, e1 in enumerate(self.elements):
            for j, e2 in enumerate(self.elements):
                if i <= j:
                    pairs.append("{}{}".format(e1, e2))
        return tuple(pairs)

    @property
    def n_rho(self):
        """Number of points at which electron density is evaluated.

        Returns:
            int
        """
        return int(self._lines[4].split()[0])

    @property
    def d_rho(self):
        """Distance between points where the electron density is evaluated.

        Returns:
            float
        """
        return float(self._lines[4].split()[1])

    @property
    def n_r(self):
        """Number of points at which interatomic potential and embedding function are evaluated.

        Returns:
            int
        """
        return int(self._lines[4].split()[2])

    @property
    def d_r(self):
        """Distance between points at which interatomic potential and embedding function are evaluated.

        Returns:
            float
        """
        return float(self._lines[4].split()[3])

    @property
    def cutoff(self):
        """Cutoff distance for all functions.

        Note:
            Measured in Angstroms.

        Returns:
            float
        """
        return float(self._lines[4].split()[4])



    def read(self):
        """Reads a setfl file."""
        body = {
            "embedding_function": {},
            "density_function": {},
            "pair_function": {}
        }

        N_body_start = 6  # setfl body ALWAYS begins on line 6
        values = []  # separate lines by spaces for multi-colummn setfl format
        for line in self._lines[N_body_start:]:
            split_line = line.split()
            for s in split_line:
                values.append(s)

        start = 0  # now start is in reference to individual values; not lines
        for e in self.elements:
            body["embedding_function"][e] = []
            body["density_function"][e] = []
            for i in range(self.n_rho):
                try:
                    float_val = float(values[start+i])
                except:
                    print("float conversion failure:")
                    print("element: ", e)
                    print("index: ", i)
                body["embedding_function"][e].append(float_val)
            start += self.n_rho
            for i in range(self.n_r):
                float_val = float(values[start+i])
                body["density_function"][e].append(float_val)
            start += self.n_r + 4  # skip the description line between elements

        start -= 4  # no description to skip between atomic and potential sections

        for ep in self.element_pairs:
            body["pair_function"][ep] = []
            for i in range(self.n_r):
                float_val = float(values[start+i])
                body["pair_function"][ep].append(float_val)
            start += self.n_r

        self._body = body

    def embedding_function(self, symbol):
        """Tabulated values of the embedding function.

        Args:
            symbol (str): Elemental symbol.

        Returns:
            list of float
        """
        return self._body["embedding_function"][symbol]

    def density_function(self, symbol):
        """Tabulated values of the density function.

        Args:
            symbol (str): Elemental symbol.

        Returns:
            list of float
        """
        return self._body["density_function"][symbol]

    def pair_function(self, symbol_pair):
        """Tabulated values of the pair function.

        Args:
            symbol_pair (str): PAir of elemental symbols
            - formatted as "{}{}".format(symbol1, symbol2)

        Returns:
            list of float
        """
        return self._body["pair_function"][symbol_pair]
