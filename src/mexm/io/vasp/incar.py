import os, shutil, pathlib
import re
import copy
import numpy as np
from collections import OrderedDict

from mexm.io.vasp.errors import VaspIncarError
from mexm.io.vasp import incartags

class Incar(object):
    format_tag = "{} = {}"
    format_tag_line = '{:<30}! {}'
    format_section = '# {:*^78}'
    
    incar_tags = {
        'ENCUT':incartags.EncutTag,
        'EDIFF':incartags.EdiffTag,
        'EDIFFG':incartags.EdiffgTag,
        'ISTART':incartags.IstartTags,
        'IBRION':incartags.IBrionTags,
        'ICHARG':incartags.IchargTags,
        'INIWAVE':incartags.IniwaveTag,
        'ISIF':incartags.IsifTag,
        'ISMEAR':incartags.IsmearTags,
        'LPLANE':incartags.LplaneTag,
        'NELM':incartags.NelmTag,
        'NELMDL':incartags.NelmdlTag,
        'NELMIN':incartags.NelminTag,
        'NPAR':incartags.NparTag,
        'NSIM':incartags.NsimTag,
        'NSW':incartags.NswTag,
        'POTIM':incartags.PotimTag,
        'PREC':incartags.PrecTags,
        'SIGMA':incartags.SigmaTag,
        'SYSTEM':incartags.SystemTag,
    }

    def __init__(self, path="INCAR"):
        """ object for dealing with input and output to VASP via INCAR file

        Args:
        filename (str): the filename of the INCAR file, default:'INCAR'
        """
        self._path = None
        self.path = path
        self.incar_tag_values = {}

        self._fmt_section = '# {:*^78}\n'
        self._fmt_arg = '{:<30}! {}\n'
        self._cmt_dict = None
        #self._cmt_dict = initialize_incar_comments()

        # default initialization of INCAR file
        self.system = 'automatically generated by mexm'
        self.__init_start_info()
        self.__init_density_of_states()
        self.__init_symmetry()
        self.__init_scf()
        self.__init_spin()
        self.__init_mixer()
        self.__init_ionic_relaxation()
        self.__init_output()

    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, path):
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        self._path = path

    def __init_start_info(self):
        self.istart = 0
        self.icharg = 0

    def __init_density_of_states(self):
        self.ismear=0
        self.sigma=0.2

    def __init_symmetry(self):
        self.isym = 2
        self.symprec = 1e-4

    def __init_scf(self):
        self.ediff = 1e-6 # convergece criteria in eV
        self.nelm = 40 # maximum number of SCF steps
        self.encut = 400 # energy cutoff
        self.prec = 'High'  # set avoid anti-aliasing errors
        self.lreal = 'False' # real space projectors are less accurate
        self.algo = 'Normal' # most robust operator

    def __init_spin(self):
        self.ispin=1
        self.lorbit=None
        self.rwigs=None
        self.magmom=None

    def __init_mixer(self):
        self.amix = 0.4
        self.bmix = 1.0
        self.amix_mag = 1.6
        self.bmix_mag = 1.0
    
    def set_mixer_settings(self):
        self.amix = 0.4
        self.amin = 0.1
        self.bmix = 1.0
        self.amix_mag = 1.6
        self.bmix_mag = 1.0

    def __init_ionic_relaxation(self):
        self.ibrion = None
        self.isif = None
        self.ediffg = None
        self.nsw = None
        self.potim = None

    def __init_output(self):
        self.lwave = False
        self.lcharg = False
        self.lvtot = False

    @property
    def is_continue_job(self):
        "bool: True if continuation job"
        if self.istart != 0 or self.icharg!=0:
            return True
        else:
            return False

    def get_section_string(self, comment):
        str_out = '# {:*^78}\n'.format(comment)
        return str_out

    def get_option_string(self, option_flag, option_value):
        try:
            option_comment = self._cmt_dict[option_flag][option_value]
            str_out = '{:<30}! {}\n'.format(
                "{} = {}".format(option_flag, option_value),
                option_comment
            )
        except KeyError:
            str_out = '{} = {}\n'.format(option_flag, option_value)
        return str_out


    def write(self, path='POSCAR'):
        """write poscar file

        Args:
        path (str): the filename of the poscar file,
        """

        self.path = path
        with open(self.path, 'w') as f:
            f.write(self.to_string())
 
    def set_tag_value(self, tag_name, tag_value):

        if isinstance(self.incar_tags[tag_name], 
                      incartags.IncarBaseFloatTag):
            tag_value_ = float(tag_value)
            assert self.incar_tag_value[tag_name].is_valid_option(
                option=tag_value
            )
            self.incar_tag_values[tag_name] = tag_value_

        elif isinstance(self.incar_tags[tag_name],
                        incartags.IncarBaseStringTag):
            assert self.incar_tag_values[tag_name].is_valid_tag(tag_value)
            self.incar_tag_values[tag_name] = tag_value_

        elif isinstance(self.incar_tags[tag_name], incartags.IncarBaseTags):
            try:
                tag_value_ = int(tag_value)
                assert self.incar_tag_value[tag_name].is_valid_option(
                    option=tag_value
                )
                self.incar_tag_values[tag_name] = int(tag_value)
            except ValueError:
                self.incar_tag_values[tag_name] = tag_value

    def get_tag_value(self, tag_name):
        return self.incar_tag_values[tag_name]

    def get_tag_comment(self, tag_name):
        tag_value = self.incar_tag_values[tag_name]
        return self.incar_tags[tag_name].get_comment()

    def read(self, path='POSCAR'):

        self.path = path
        f = open(self.filename)
        for line in f:
            if line.startswith('#'):
                # ignore comments
                pass
            elif line.strip() == '':
                # ignore blank lines
                pass
            else:
                args = [ line.strip().split('!')[0].split('=')[0].strip(),
                         line.strip().split('!')[0].split('=')[1].strip() ]
                tag_name = args[0]
                tag_value = args[1]
                self.set_tag_value(tag_name=tag_name, tag_value=tag_value)
                if args[0] == 'ISTART':
                    self.istart = int(args[1])
                elif args[0] == 'ICHARG':
                    self.icharg = int(args[1])
                elif args[0] == 'ISPIN':
                    self.ispin = int(args[1])
                elif args[0] == 'MAGMOM':
                    self.magmom = args[1]
                elif args[0] == 'ISMEAR':
                    self.ismear = int(args[1])
                elif args[0] == 'SIGMA':
                    self.sigma = float(args[1])
                elif args[0] == 'ALGO':
                    self.algo = args[1]
                elif args[0] == 'EDIFF':
                    self.ediff = float(args[1])
                elif args[0] == 'ENCUT':
                    self.encut = float(args[1])
                elif args[0] == 'NELM':
                    self.nelm == int(args[1])
                elif args[0] == 'PREC':
                    self.prec = args[1]
                elif args[0] == 'EDIFFG':
                    self.ediffg = float(args[1])
                elif args[0] == 'IBRION':
                    self.ibrion = int(args[1])
                elif args[0] == 'ISIF':
                    self.isif = int(args[1])
                elif args[0] == 'POTIM':
                    self.potim = float(args[1])
                elif args[0] == 'NSW':
                    self.nsw = int(args[1])
                elif args[0] == 'SYSTEM':
                    self.system = args[1]
                elif args[0] == 'LWAVE':
                    self.lwave = args[1]
                elif args[0] == 'LCHARG':
                    self.lcharg = args[1]
                elif args[0] == 'LORBIT':
                    self.lorbit = int(args[1])
                elif args[0] == 'LVTOT':
                    self.lvtot = args[1]
                elif args[0] == 'LREAL':
                    self.lreal = args[1]
                elif args[0] == 'MAGMOM':
                    self.magmom = args[1]
                elif args[0] == 'ISYM':
                    self.isym = int(args[1])
                elif args[0] == 'SYMPREC':
                    self.symprec = float(args[1])
                elif args[0] == 'RWIGS':
                    self.rwigs = float(rwigs)
                elif args[0] == 'NPAR':
                    self.npar = int(args[1])
                elif args[0] == "AMIX":
                    self.amix = float(args[1])
                elif args[0] == 'BMIX':
                    self.bmix = float(args[1])
                elif args[0] == 'AMIX_MAG':
                    self.amix_mag = float(args[1])
                elif args[1] == 'BMIX_MAG':
                    self.bmix_mag = float(args[1])
                elif args[0] == 'LREAL':
                    self.lreal = args[1]
                elif args[0] == 'LPLANE':
                    self.lplane = args[1]
                elif args[0] == 'NSIM':
                    self.nsim = int(args[1])
                elif args[0] == 'INIWAVE':
                    self.iniwave = int(args[1])
                elif args[0] == 'NELMIN':
                    self.nelmmin = int(args[1])
                elif args[0] == 'NELMDL':
                    self.nelmdl = int(args[1])
                else:
                    err_msg = "pypospack does not support tag {}".format(args[0])
                    raise VaspIncarError(err_msg)
        f.close()

    def set_relaxation_type(self, relaxation_type):
        relaxation_types_dict = {
            'all':self.set_ionic_relaxation_none,
            'volume':self.set_ionic_relaxation_volume,
            'position':self.set_ionic_relaxation_positions,
            'none':self.set_ionic_relaxation_none
        }
        relaxation_types_dict[relaxation_type]()

    def set_ionic_relaxation_none(self):
        self.ibrion = None
        self.isif = None

    def set_ionic_relaxation_volume(self):
        self.ibrion = None
        self.isif = None

    def set_ionic_relaxation_positions(self):
        self.ibrion = None
        self.isif = None

    def set_ionic_relaxation_all(self):
        self.ibrion = None
        self.isif = None

    def to_string(self):
        str_out = ''
        str_out += self.system_information_to_string_()
        str_out += self.start_information_to_string_()
        str_out += self.dos_information_to_string_()
        str_out += self.__sym_information_to_string()
        str_out += self.__scf_information_to_string()
        str_out += self.__spin_polarization_to_string()
        str_out += self._mixer_to_string()
        str_out += self.__ionic_relaxation_to_string()
        str_out += self.__output_configuration_to_string()
        return str_out

    def get_tag_string_(self, tag_name, tag_value):
        fmt_line = self.format_tag_line
        fmt_tag = self.format_tag

        tag_comment = self.incar_tags[tag_name].get_comment(tag_value)
        return fmt_line.format(fmt_tag.format(tag_name, tag_value),
                               tag_comment)

    def system_information_to_string_(self):
        str_out = "SYSTEM = {}\n\n".format(self.system)
        return str_out

    def start_information_to_string_(self):
        fmt_section = self.format_section

        str_out = "\n".join([
            fmt_section.format('STARTING INFORMATION'),
            self.get_tag_string_('ISTART', self.istart),
            self.get_tag_string_('ICHARG', self.icharg)
        ]) + "\n"

        return str_out

    def dos_information_to_string_(self):
        fmt_section = self.format_section

        str_out = "\n".join([
            fmt_section.format('DENSITY OF STATES'),
            self.get_tag_string_('ISMEAR', self.istart),
            self.get_tag_string_('SIGMA', self.icharg)
        ]) + "\n"

        return str_out



    def _mixer_to_string(self):

        mixing_tags = [self.amix, self.bmix, self.amix_mag, self.bmix_mag]
        if all([k is None for k in mixing_tags]):
            return ""
        else:
            str_out = self.get_section_string("MIXING")
            if self.amix is not None:
                str_out += self.get_option_string('AMIX',self.amix)
            if self.bmix is not None:
                str_out += self.get_option_string('BMIX',self.bmix)
            if self.amix_mag is not None:
                str_out += self.get_option_string('AMIX_MAG', self.amix_mag)
            if self.bmix_mag is not None:
                str_out += self.get_option_string('BMIX_MAG', self.bmix_mag)
            return str_out
    def __system_information_to_string(self):
        str_out = "SYSTEM = {}\n\n".format(self.system)
        return str_out





    def __sym_information_to_string(self):
        fmt = "{} = {}"
        str_out = self._fmt_section.format('SYMMETRY')
        str_out += self._fmt_arg.format(fmt.format('ISYM',self.isym),self._cmt_dict['ISYM'][self.isym])
        str_out += self._fmt_arg.format(fmt.format('SYMPREC',self.symprec),self._cmt_dict['SYMPREC'])
        str_out += "\n"
        return str_out


    def __scf_information_to_string(self):
        fmt = "{} = {}"
        if self.algo.startswith('N'):
            self.algo = 'Normal'
        elif self.algo.startswith('V'):
            self.algo = 'VeryFast'
        elif self.algo.startswith('F'):
            self.algo = 'Fast'
        else:
            raise VaspIncarError('Unsupported ALGO value:{}'.format(self.algo))

        if self.lreal == False or self.lreal.startswith('F') or self.lreal == '.FALSE.':
            self.lreal = '.FALSE.'
        elif self.lreal == True or self.lreal.startswith('T') or self.lreal == '.TRUE.':
            self.lreal = '.TRUE.'
        else:
            str_type = type(self.lreal)
            str_value = '{}'.format(self.lreal)
            print(str_type,str_value)
            raise VaspIncarError('Unsupported LREAL value:{}'.format(self.lreal))

        str_out = self._fmt_section.format('ELECTRONIC SCF RELAXATION')
        str_out += self._fmt_arg.format(fmt.format('ALGO',self.algo),self._cmt_dict['ALGO'][self.algo])
        str_out += self._fmt_arg.format(fmt.format('PREC',self.prec),self._cmt_dict['PREC'][self.prec])
        str_out += self._fmt_arg.format(fmt.format('LREAL',self.lreal),self._cmt_dict['LREAL'][self.lreal])
        str_out += self._fmt_arg.format(fmt.format('EDIFF',self.ediff),self._cmt_dict['EDIFF'])
        str_out += self._fmt_arg.format(fmt.format('ENCUT',self.encut),self._cmt_dict['ENCUT'])
        str_out += self._fmt_arg.format(fmt.format('NELM',self.nelm),self._cmt_dict['NELM'])
        str_out += '\n'

        return str_out

    def _spin_polarization_to_string(self):
        fmt = "{} = {}"

        str_out = self._fmt_section.format('SPIN POLARIZATION CONFIGURATION')

        if self.ispin==1:
            str_out += self._fmt_arg.format(fmt.format('ISPIN',self.ispin),self._cmt_dict['ISPIN'][self.ispin])

        if self.ispin == 2:
            str_out += self._fmt_arg.format(fmt.format('ISPIN',self.ispin),self._cmt_dict['ISPIN'][self.ispin])

            if self.lorbit is not None:
                if self.lorbit < 10:
                    if self.rwigs is not None:
                        str_out += self.get_option_string('LORBIT',self.lorbit)
                        str_out += self.get_option_string('RWIGS',self.rwigs)
                    else:
                        if self.lorbit == 0:
                            self.lorbit = 10
                        elif self.lorbit == 1:
                            self.lorbit = 11
                        elif self.lorbit == 2:
                            self.lorbit = 12
                        elif self.lorbit == 5:
                            self.lorbit = 10
                        else:
                            raise VaspIncarError('')
                        str_out += self.get_option_string('LORBIT',self.lorbit)
                else:
                    str_out += self.get_option_string('LORBIT',self.lorbit)

            if self.magmom is not None:
                str_out += fmt.format('MAGMOM',self.magmom) + '\n'

        str_out += '\n'

        return str_out

    @DeprecationWarning
    def __spin_polarization_to_string(self):
        return self._spin_polarization_to_string()

    def __ionic_relaxation_to_string(self):
        fmt = "{} = {}"

        if (self.ibrion is None) and (self.isif is None):
            return ''

        # some default configuration for ibrion
        if self.ibrion is None:
            self.ibrion = 2

        # some default configuration for isif
        if self.isif is None:
            self.isif = 3

        # some default configuration for EDIFFG
        if self.ediffg is None:
            self.ediffg = -0.01 # ev/A - typical
        # some default configuration for POTIM
        if self.potim is None:
            if self.ibrion in [1,2,3]:
                self.potim = 0.5
            if self.ibrion in [5,6,7,8]:
                self.potim = 0.015

        # some default configuration for NSW
        if self.nsw is None:
            self.nsw = 40

        str_out = self._fmt_section.format('IONIC RELAXATION CONFIGURATION')
        str_out += self._fmt_arg.format(fmt.format('IBRION',self.ibrion),self._cmt_dict['IBRION'][self.ibrion])
        str_out += self._fmt_arg.format(fmt.format('ISIF',self.isif),self._cmt_dict['ISIF'][self.isif])
        str_out += self._fmt_arg.format(fmt.format('POTIM',self.potim),self._cmt_dict['POTIM'])
        str_out += self._fmt_arg.format(fmt.format('NSW',self.nsw),self._cmt_dict['NSW'])

        if self.ediffg < 0:
            str_out += self._fmt_arg.format(fmt.format('EDIFFG',self.ediffg),'force convergence requirements in ev A')
        else:
            str_out += self._fmt_arg.format(fmt.format('EDIFGG',self.ediffg),'energy convergence in eV')
        str_out += '\n'

        return str_out

    def __output_configuration_to_string(self):
        fmt = "{} = {}"

        if self.lwave in [True,'T','.TRUE.']:
            self.lwave = '.TRUE.'
        elif self.lwave in [False,'F','.FALSE.']:
            self.lwave = '.FALSE.'
        else:
            msg = "LWAVE tag cannot be {}({})".format(type(self.lwave),self.lwave)
            raise VaspIncarException(msg)

        if self.lcharg in [True,'T','.TRUE.']:
            self.lcharg = '.TRUE.'
        elif self.lcharg in [False,'F','.FALSE.']:
            self.lcharg = '.FALSE.'
        else:
            msg = "LCHARG tag cannot be {}({})".format(type(self.lcharg),self.lcharg)
            raise VaspIncarException(msg)

        if self.lvtot is [True,'T','.TRUE.']:
            self.lvtot = '.TRUE.'
        elif self.lvtot in [False,'T','.FALSE.']:
            self.lvtot= '.FALSE.'
        else:
            msg = "LVTOT tag cannot be {}({})".format(type(self.lwave),self.lvtot)
            raise VaspIncarException(msg)

        str_out = self._fmt_section.format('OUTPUT CONFIGURATION')
        str_out += self._fmt_arg.format(fmt.format('LWAVE',self.lwave),self._cmt_dict['LWAVE'][self.lwave])
        str_out += self._fmt_arg.format(fmt.format('LCHARG',self.lcharg),self._cmt_dict['LCHARG'][self.lcharg])
        str_out += self._fmt_arg.format(fmt.format('LVTOT',self.lvtot),self._cmt_dict['LVTOT'][self.lvtot])
        str_out += "\n"
        return str_out

# *****************************************************************************
# ****    SOME HELPER FUNCTIONS
# *****************************************************************************



