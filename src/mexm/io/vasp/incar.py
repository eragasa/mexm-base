# coding: utf-8
# Copyright (c) Eugene J. Ragasa
# Distributed under the terms of the MIT License

""" the INCAR file for VASP
"""

__all__ = ["Incar"]
__author__ = "Eugene J. Ragasa"
__email__ = "ragasa.2@osu.edu"
__copyright__ = "Copyright 2020, Eugene J. Ragasa"
__maintainer__ = "Eugene J. Ragasa"
__date__ = "2020/02/22"

import os
import shutil
import pathlib
import re
import copy
import numpy as np
from collections import OrderedDict

from mexm.io.vasp.errors import VaspIncarError
from mexm.io.vasp import incartags

class Incar(object):
    """ object for creating and reading INCAR files for VASP

    Attributes:
        incar_tag_values (dict): the key the tag_name, the value is the 
            tag value.

    """
    format_tag = "{} = {}"
    format_tag_line = '{:<30}! {}'
    format_section = '# {:*^78}'
    
    incar_tags = {
        'ALGO':incartags.AlgoTag,
        'AMIX':incartags.AmixTag,
        'AMIX_MAG':incartags.AmixmagTag,
        'BMIX':incartags.BmixTag,
        'BMIX_MAG':incartags.BmixmagTag,
        'ENCUT':incartags.EncutTag,
        'EDIFF':incartags.EdiffTag,
        'EDIFFG':incartags.EdiffgTag,
        'ISTART':incartags.IstartTag,
        'IBRION':incartags.IbrionTag,
        'ICHARG':incartags.IchargTag,
        'INIWAVE':incartags.IniwaveTag,
        'ISIF':incartags.IsifTag,
        'ISMEAR':incartags.IsmearTag,
        'ISPIN':incartags.IspinTag,
        'ISYM':incartags.IsymTag,
        'LCHARG':incartags.LchargTag,
        'LPLANE':incartags.LplaneTag,
        'LREAL':incartags.LrealTags,
        'LWAVE':incartags.LwaveTag,
        'LVTOT':incartags.LvtotTag,
        'KPAR':incartags.KparTag,
        'NELM':incartags.NelmTag,
        'NELMDL':incartags.NelmdlTag,
        'NELMIN':incartags.NelminTag,
        'NPAR':incartags.NparTag,
        'NSIM':incartags.NsimTag,
        'NSW':incartags.NswTag,
        'POTIM':incartags.PotimTag,
        'PREC':incartags.PrecTag,
        'SIGMA':incartags.SigmaTag,
        'SYMPREC':incartags.SymprecTag,
        'SYSTEM':incartags.SystemTag,
    }

    def __init__(self, path=None):
        """ object for dealing with input and output to VASP via INCAR file

        Args:
            filename (str): the filename of the INCAR file, default:'INCAR'
        """
        self._path = None

        self._lwave = None
        self._lcharg = None
        self._lvtot = None


        # handle arguments
        if path is not None:
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
        """str: the path to the INCAR file"""
        return self._path
    
    @path.setter
    def path(self, path):
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        self._path = path

    @property
    def lwave(self):
        return self._lwave

    @lwave.setter
    def lwave(self, lwave):
        if lwave in [True, 'T', '.TRUE.']:
            self._lwave = '.TRUE.'
        elif lwave in [False, 'F', '.FALSE.']:
            self._lwave = '.FALSE.'
        else:
            msg = "LWAVE tag cannot be {}({})".format(type(self.lwave),self.lwave)
            raise VaspIncarError(msg)

    @property
    def lcharg(self):
        return self._lcharg
        
    @lcharg.setter
    def lcharg(self, lcharg):
        if lcharg in [True, 'T', '.TRUE.']:
            self._lcharg = '.TRUE.'
        elif lcharg in [False, 'F', '.FALSE.']:
            self._lcharg = '.FALSE.'
        else:
            msg = "LCHARG tag cannot be {}({})".format(type(self.lcharg),self.lcharg)
            raise VaspIncarError(msg)

    @property
    def lvtot(self):
        return self._lvtot

    @lvtot.setter
    def lvtot(self, lvtot):
        if lvtot in [True, 'T', '.TRUE']:
            self._lvtot = '.TRUE.'
        elif lvtot in [False, 'F', '.FALSE.']:
            self._lvtot = '.FALSE.'
        else:
            msg = "LVTOT tag cannot be {}({})".format(type(self.lwave),self.lvtot)
            raise VaspIncarError(msg)

    @property
    def icharg(self):
        return self.incar_tag_values['ICHARG']

    @icharg.setter
    def icharg(self, icharg):
        self.incar_tag_values['ICHARG'] = icharg

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

    def get_option_string(self, option_tag, option_value):
        """

        Args:
           option_flag (str):
        """
        try:
            option_comment = self.incar_tags[option_tag].get_comment(option_value)
            str_out = '{:<30}! {}\n'.format(
                "{} = {}".format(option_tag, option_value),
                option_comment
            )
        except KeyError:
            str_out = '{} = {}\n'.format(option_tag, option_value)
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

        # IncarBaseFloatTag
        if issubclass(self.incar_tags[tag_name], incartags.IncarBaseFloatTag):

            tag_value_ = float(tag_value)
            if not self.incar_tags[tag_name].is_valid_option(option=tag_value_):
                msg = "{tag_name} = {tag_value} is not a valid option"
                raise ValueError(
                    msg.format(tag_name=tag_name, tag_value=tag_value)
                )
            self.incar_tag_values[tag_name] = tag_value_

        # IncarBaseIntegerTag
        elif issubclass(self.incar_tags[tag_name], incartags.IncarBaseIntegerTag):

            tag_value_ = int(tag_value)
            if not self.incar_tags[tag_name].is_valid_option(option=tag_value_):
                msg = "{tag_name} = {tag_value} is not a valid option"
                raise ValueError(
                    msg.format(tag_name=tag_name, tag_value=tag_value)
                )
            self.incar_tag_values[tag_name] = tag_value_

        # IncarBaseStringTag
        elif issubclass(self.incar_tags[tag_name], incartags.IncarBaseStringTag):
            if not self.incar_tags[tag_name].is_valid_option(
                option=tag_value
            ):
                msg = "{tag_name} = {tag_value} is not a valid option"
                raise ValueError(
                    msg.format(tag_name=tag_name, tag_value=tag_value)
                )
            
            tag_value_ = str(tag_value)
            self.incar_tag_values[tag_name] = tag_value_

        # IncarBaseEnumeratedTag
        elif issubclass(self.incar_tags[tag_name], incartags.IncarBaseEnumeratedTag):
            tag_value_ = self.incar_tags[tag_name].convert(option=tag_value)
            if not self.incar_tags[tag_name].is_valid_option(option=tag_value_):
                msg = "{tag_name} = {tag_value} is not a valid option"
                raise ValueError(
                    msg.format(tag_name=tag_name, tag_value=tag_value)
                )
            
            self.incar_tag_values[tag_name] = tag_value_

        # IncarBaseTags
        elif issubclass(self.incar_tags[tag_name], incartags.IncarBaseTag):
            if not self.incar_tags[tag_name].is_valid_option(option=tag_value):
                msg = "{tag_name} = {tag_value} is not a valid option"
                raise ValueError(
                    msg.format(tag_name=tag_name, tag_value=tag_value)
                )

            self.incar_tag_values[tag_name] = tag_value_
                    
        else:
            msg = "{tag_name},{tag_class},{tag_value}".format(
                tag_name=tag_name,
                tag_class=str(self.incar_tags[tag_name]),
                tag_value=tag_value
            )
            raise VaspIncarError(msg)

    def get_tag_value(self, tag_name: str):
        """ get the tag value for the INCAR file
        
        Arguments:
            tag_name (str): name of the INCAR tag
        Returns:
            tag value for the incar file
        """
        return self.incar_tag_values[tag_name]

    def get_tag_comment(
        self, 
        tag_name: str, 
        tag_value: (str, int, float, list) = None
    ):
        """ get the tag comment for a value of the incar file 
        
        Arguments:
            tag_name (str): name of the INCAR tag
            tag_value (str, int, float, list): value of the 
                INCAR file
        Returns:
            str: comment for the INCAR tag 
        """
        tag_name_ = self.incar_tag_values[tag_name]
        return self.incar_tags[tag_name_].get_comment()

    def read(self, path=None):
        """ configure the object from reading an INCAR file

        Args:
           path (str): path to POSCAR file. Default value is None
        """
        if path is not None:
            self.path = path
        
        f = open(self.path, 'r')
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
        str_out += self.optimization_information_to_string()
        str_out += self.start_information_to_string_()
        str_out += self.dos_information_to_string_()
        str_out += self.symmetry_information_to_string()
        str_out += self.scf_information_to_string()
        str_out += self.spin_polarization_to_string()
        str_out += self._mixer_to_string()
        str_out += self.__ionic_relaxation_to_string()
        str_out += self.output_configuration_to_string()
        return str_out

    def get_tag_comment_(self, tag_name, tag_value):
        return self.incar_tags[tag_name].get_comment(tag_value)

    def get_tag_string_(self, tag_name, tag_value):
        fmt_line = self.format_tag_line
        fmt_tag = self.format_tag

        tag_comment = self.get_tag_comment_(
            tag_name=tag_name,
            tag_value=tag_value
        )

        return fmt_line.format(
            fmt_tag.format(tag_name, tag_value),
            tag_comment)

    def get_section_string(self, section_name, section_included_tags):
        fmt_section = self.format_section
          
        str_out = fmt_section.format(section_name) + "\n"
        for k in section_included_tags:
            if k in self.incar_tag_values:
                str_out += self.get_option_string(
                    option_tag = k, 
                    option_value = self.incar_tag_values[k]
                )
            else:
                pass
        return str_out

        
    def system_information_to_string_(self):
        str_out = "SYSTEM = {}\n".format(self.system)
        return str_out

    def start_information_to_string_(self):
        section_name = 'STARTING INFORMATION'
        section_included_tags = ['ISTART', 'ICHARG']
        str_out = self.get_section_string(
            section_name = section_name,
            section_included_tags = section_included_tags
        )
        return str_out

    def optimization_information_to_string(self):
        section_name = 'OPTIMIZATION'
        section_included_tags = ['LPLANE', 'NPAR', 'NSIM', 'KPAR']
        str_out = self.get_section_string(
            section_name = section_name,
            section_included_tags = section_included_tags
        )
        return str_out

    def dos_information_to_string_(self):
        section_name = 'DENSITY OF STATES'
        section_included_tags = ['ISMEAR', 'SIGMA']
        str_out = self.get_section_string(
            section_name = section_name,
            section_included_tags = section_included_tags
        )
        return str_out

    def symmetry_information_to_string(self):
        section_name = 'SYMMETRY'
        section_included_tags = ['ISYM', 'SYMPREC']
        if 'ISYM' not in self.incar_tag_values:
            self.incar_tag_values['ISYM'] = -1
        str_out = self.get_section_string(
            section_name = section_name,
            section_included_tags = section_included_tags
        )
        return str_out

    def scf_information_to_string(self):
        section_name = 'ELECTRONIC SCF RELATION'
        section_included_tags = [
            'ALGO', 'PREC', 'LREAL', 'EDIFF', 'ENCUT', 'NELM',
            'NELMMIN', 'NELMDL'
        ]
        str_out = self.get_section_string(
            section_name = section_name,
            section_included_tags = section_included_tags
        )
        return str_out

    def spin_polarization_to_string(self):
        fmt = "{} = {}"

    
        if self.ispin==1:
            fmt_section = self.format_section

            section_name = 'SPIN POLARIZATION CONFIGURATION'

            str_out = "\n".join([
                fmt_section.format(section_name),
                self.get_tag_string_('ISPIN', self.ispin)
            ]) + "\n"

            return str_out

        if self.ispin == 2:
            fmt_section = self.format_section
            str_out = self._fmt_section.format('SPIN POLARIZATION CONFIGURATION')
            str_out += self.get_tag_string_('ISPIN', self.ispin)
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

    def output_configuration_to_string(self):
        fmt_section = self.format_section

        section_str = 'OUTPUT CONFIGURATION'

        str_out = "\n".join([
            fmt_section.format(section_str),
            self.get_tag_string_('LWAVE', self.lwave),
            self.get_tag_string_('LCHARG', self.lcharg),
            self.get_tag_string_('LVTOT', self.lvtot)
        ]) + "\n"

        return str_out


    def _mixer_to_string(self):
        section_name = "MIXING"
        section_included_tags = [
            'AMIX', 'BMIX',
            'AMIX_MAG', 'BMIX_MAG'
        ]
        if not any(
            [k in self.incar_tag_values for k in section_included_tags]
        ):
            return ""

        str_out = self.get_section_string(
            section_name = section_name,
            section_included_tags = section_included_tags
        )
        return str_out

    def get_default_potim(self):
        if self.ibrion in [1, 2, 3]:
            self.potim = 0.5
        elif self.ibrion in [5, 6, 7, 8]:
            self.potim = 0.015
        else:
            msg = ('IBRION illegal tag error: {}'.format(self.ibrion))
            raise VaspIncarError(msg)

    def get_default_ediffg(self):
        ediffg = -0.01 # eV/Angs - typical value
        return ediffg

    def get_default_nsw(self):
        nsw = 40
        return nsw

    def __ionic_relaxation_to_string(self):
        
        # set a default value of ISIF, if one is not set
        if 'IBRION' not in self.incar_tag_values:
            self.incar_tag_values['IBRION'] = -1
        
        if self.incar_tag_values['IBRION'] == -1:
            fmt_section = self.format_section
            section_name = 'IONIC RELAXATION CONFIGURATION'
            section_included_tags = ['IBRION']
            str_out = self.get_section_string(
                section_name = section_name,
                section_included_tags = section_included_tags
            )
            return str_out

        else:

            fmt_section = self.format_section
            section_name = 'IONIC RELAXATION CONFIGURATION'
            section_included_tags = [
                'IBRION', 'ISIF', 'POTIM', 'NSW', 'EDIFFG'
            ]
            str_out = fmt_section.format(section_name) + "\n"
            str_out = self.get_section_string(
                section_name = section_name,
                section_included_tags = section_included_tags
            )
            return str_out
# *****************************************************************************
# ****    SOME HELPER FUNCTIONS
# *****************************************************************************



