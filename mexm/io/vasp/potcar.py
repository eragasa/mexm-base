import os

class VaspPotcarError(Exception):
    def __init__(self,*args,**kwargs):
        """ Error class for reading/writing VASP POTCAR IO issues """
        Exception.__init__(self,*args,**kwargs)

class Potcar(object):
    """ object to deal with POTCAR files for VASP simulations

    Args:
        symbols (:obj:`list` of :obj:`str`): a list of chemical symbols
        path (str): the path of the POTCAR
        xc (str): the exchange correlation model.  Default is 'GGA'

    Attributes:
        potcar_dir (str): the path of the VASP potential directory.
        potcars (dict): a dictionary of key-value pairs of symbols to potcar
            type where the key value is the ISO symbol, and the value is the
            the psuedopotnetial type.

    If an :obj:`str` is passed into symbols, then the string will be
    cast into a :obj:`list` of :obj:`str`

    A directory of potentials is not included in pypospack because it is
    protected by copy right.  If the potcar_dir is not set, then pypospack
    will use the environment variables:

    For linux style sytems:
    >>> export VASP_LDA_DIR=$(cd ~/opt/vasp/potentials/LDA;pwd)
    >>> export VASP_GGA_DIR=$(cd ~/opt/vasp/potentials/GGA;pwd)

    for windows systems:
    >>> setx VASP_LDA_DIR "C:\vasp\LDA" /M
    >>> setx VASP_GGA_DIR "C:\vasp\GGA" /M
    """
    def __init__(self, symbols = None,
                       path= None,
                       xc = 'GGA',
                       potcars = None):
        self.potcar_dir = None

        self.path = None
        self.symbols = None
        self.potcars = None

        if path is not None:
            self.path = path

        if isinstance(symbols,str):
            self.symbols = [symbols]
        else:
            try:
                self.symbols = [s for s in symbols]
            except:
                msg = 'symbols type{}={}'.format(type(symbols),symbols)

        if potcars is not None:
            self.potcars = potcars.copy()
        self.xc = xc
        self.encut_min = []
        self.encut_max = []
        self.models    = []
        self.exch      = []

    def read(self, path = "POTCAR"):
        # initialize arrays
        self.symbols   = []
        self.encut_min = []
        self.enmin_max = []
        self.models = []
        self.xc      = []

        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if 'TITEL' in line:
                    symbol = line.split('=')[1].strip().split(' ')[1]
                    self.symbols.append(symbol)
                elif 'ENMIN' in line:
                    obj_re = re.match('ENMAX  =  (.*); ENMIN  =  (.*) eV.*',line,re.M|re.I)
                    enmax = float(obj_re.group(1))
                    enmin = float(obj_re.group(2))
                    self.encut_min.append(enmin)
                    self.encut_max.append(enmax)
                elif 'LEXCH' in line:
                    xc = line.split('=')[1].strip()
                    self.xc.append(xc)
                elif "VRHFIN" in line:
                    m = line.split('=')[1].strip()
                    self.models.append(m)

    def write(self, 
              path = 'POTCAR', 
              src = None, 
              potcars = None):
        """ write POTCAR file

        Arguments:
            path (str): If none, then the method will use the internal
                attribute.  Other

        Raises:
            pypospack.io.vasp.VaspPotcarError
        """
        if path is not None:
            self.path = path
        else:
            if self.path is None:
                raise TypeError('cannot find suitable path')

        #  if a source potcar is given just copy the file
        if src is not None:
            __write_potcar_by_copy(src_fn=src,dst_fn=self.path)

        self.__set_xc_directory()

        #  get full path of potcars
        if potcars is not None:
            self.potcars = potcars.copy()
        else:
            self.__find_potcar_files()


        with open(self.path,'w') as f_out:
            for s in self.symbols:
                with open(self.potcars[s],'r') as f_in:
                    # avoid reading large files into memory
                    chunk_sz = 1024*1024*10 # 10MB
                    shutil.copyfileobj(f_in,f_out, chunk_sz)

    def __write_potcar_by_copy(self,src_fn,dst_fn):
        with open(dst_fn) as f_out:
            with open(src_fn) as f_in:
                chunk_sz = 1024*1024*10
                shutil.copyfileobj(f_in,f_out,chunk_sz)

    def __find_potcar_files(self):
        # a more intelligent way of selecting potcars based upon VASP
        # recommendations should be implemented
        # http://cms.mpi.univie.ac.at/vasp/vasp/Recommended_PAW_potentials_DFT_calculations_using_vasp_5_2.html
        self.potcars = {} # initialize
        for s in self.symbols:
            # try VASP_XC_DIR/symbol/POTCAR
            if pathlib.Path(os.path.join(self.potcar_dir,s,'POTCAR')).is_file():
                self.potcars[s] = os.path.join(self.potcar_dir,s,'POTCAR')
            # try VASP_XC_DIR/symbol_new/POTCAR
            elif pathlib.Path(os.path.join(self.potcar_dir,"{}_new".format(s),'POTCAR')).is_file():
                self.potcars[s] = os.path.join(self.potcar_dir,"{}_new".format(s),'POTCAR')
            # try VASP_XC_DIR/symbols_h/POTCAR
            elif pathlib.Path(os.path.join(self.potcar_dir,"{}_h".format(s),'POTCAR')).is_file():
                self.potcars[s] = os.path.join(self.potcar_dir,"{}_h".format(s),'POTCAR')
            else:
                print(os.path.join(self.potcar_dir,"{}_new".format(s),'POTCAR'))
                msg = 'cannot find a POTCAR file for {}.{}\n'.format(self.xc,s)
                msg += 'potcar_dir:{}'.format(self.potcar_dir)
                raise VaspPotcarError(msg)

    @staticmethod
    def get_xc_directory(self, xc_type):
        if xc_type == 'GGA':
            try:
                return os.environ['VASP_GGA_DIR']
            except KeyError:
                msg = (
                    'need to set the environment variable VASP_GGA_DIR'
                )
                raise VaspPotcarError(msg)
        elif xc_type == 'LDA':
            try:
                return os.environ['VASP_LDA_DIR']
            except KeyError:
                msg = (
                    'need to set the environment variable VASP_LDA_DIR'
                )
                raise VaspPotcarError(msg)
        else:
            msg = (
                'unknown xc_type:{}'
            ).format(xc_type)
            raise VaspPotcarError(msg)
        
    def __set_xc_directory(self):
        """ sets the directory of the exchange correlation functional

        the exchange correlation functional is set to either 'LDA' or 'GGA'
        based upon environment variables

        Raises:
            (pypospack.io.vasp.VaspPotcarError): if the directory is not set
                 as an environment variable.
        """
        if self.xc == 'GGA':
            try:
                self.potcar_dir = os.environ['VASP_GGA_DIR']
            except KeyError:
                msg = ('need to set environment variable VASP_GGA_DIR to the '
                       'location of the VASP GGA-PBE potential files' )
                raise VaspPotcarError(msg)
        elif self.xc == 'LDA':
            try:
                self.potcar_dir = os.environ['VASP_LDA_DIR']
            except KeyError:
                msg = ('need to set environment variable VASP_LDA_DIR to the '
                       'location of the VASP LDA-CA potential files' )

    def __str__(self):
        header_row   = "symbol enmin enmax xc\n"
        format_row   = "{}({}) {:10.6f} {:10.6f} {}\n"

        n_atoms = len(self._symbols)
        str_out      = header_row
        for i in range(n_atoms):
            str_out += format_row.format(self._symbols[i],
                                         self._models[i],
                                         self._encut_min[i],
                                         self._encut_max[i],
                                         self._xc[i])
        return str_out

def get_recommmended_potcars(symbols):
    # standard recommendations
    potcar_std = {
        'H':'H',
        'He':'He',
        'Li':'Li_sv',
        'Be':'Be',
        'B':'B',
        'C':'C'
    }
