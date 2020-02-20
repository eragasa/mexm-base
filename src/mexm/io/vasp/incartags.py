from collections import OrderedDict
from mexm.io.vasp.errors import VaspIncarError

class IncarBaseTag():
    tag_dictionary = OrderedDict()

    @classmethod
    def is_valid_option(cls, option):
        if option in cls.tag_dictionary:
            return True
        else:
            return False

    @classmethod
    def get_comment(cls, option):
        try:
            return cls.tag_dictionary[option]
        except KeyError:
            msg = "unknown option, {}".format(option)
            raise VaspIncarError(msg)


class IncarBaseTags(IncarBaseTag): pass

class IncarBaseEnumeratedTag(IncarBaseTag):
    tag_name = 'fake_tag'
    tag_dictionary = {}

    @classmethod
    def is_valid_option(cls, option):
        if option in cls.tag_dictionary:
            return True
        else:
            return False

class IncarBaseIntegerTag(IncarBaseTag):
    tag_name = "fake_tag"
    comment = ""

    @classmethod
    def is_valid_option(cls, option):
        return isinstance(option, int)

    @classmethod
    def get_comment(cls, option):
        return cls.comment

class IncarBaseStringTag(IncarBaseTag):
    tag_name = "fake tag"
    comment = ""

    @classmethod
    def is_valid_option(cls, option):
        return isinstance(option, str)

    @classmethod
    def get_comment(cls, option):
        raise NotImplementedError

class IncarBaseFloatTag(IncarBaseTag):
    tag_name = 'fake tag'
    comment = 'fake comment'

    @classmethod
    def is_valid_option(cls, option):
        if any([
                isinstance(option,int),
                isinstance(option,float)
                ]):
            return True
        else:
            return False

    @classmethod
    def get_comment(cls, option):
        return cls.comment

class EdiffTag(IncarBaseFloatTag):
    tag_name = 'EDIFF'
    comment = 'convergence condition for SC-loop in eV'

class EdiffgTag(IncarBaseFloatTag):
    tag_name = 'EDIFFG'
    comment_force_relaxation = 'force convergence requirements in ev A'
    comment_energy_relaxation = 'energy convergence in eV'

    @classmethod
    def is_valid_option(cls, option):
        try:
            option_ = float(option)
        except ValueError:
            return False

        if option_ == 0:
            return False
        else:
            return True
        
    @classmethod
    def get_comment(cls,option):
        try:
            option_ = float(option)
        except ValueError:
            msg = 'value must be castable into a float'
            raise TypeError(msg)

        if option == 0:
            msg = 'cannot select zero, must select a convergence value'
            raise ValueError(msg)
        elif option_ < 0:
            return cls.comment_force_relaxation
        else:
            return cls.comment_energy_relaxation

class EncutTag(IncarBaseFloatTag):
    tag_name = 'ENCUT'
    comment = 'Cut-off energy for plane wave basis set in eV'

    @classmethod
    def is_valid_option(cls, option):
        try:
            option_ = float(option)
        except ValueError:
            return False
        
        if option > 0:
            return True
        else:
            return False

class IniwaveTag(IncarBaseIntegerTag):
    tag_name = 'INIWAV'
    tag_dictionary = OrderedDict([
        (0, 'jellium wave functions'),
        (1, 'random wave functions')
    ])

    @classmethod
    def is_valid_option(cls, option):
        return option in cls.tag_dictionary

class IstartTags(IncarBaseTags):
    tag_name = 'ISTART'
    tag_dictionary = OrderedDict([
        (0,'begin from scratch'),
        (1,'continuation job, constant energy cutoff'),
        (2,'continuation job, constant basis set'),
    ])

class IsymTags(IncarBaseTags):

    tag_dictionary = OrderedDict([
        (-1,'symmetry off'),
        (0,'symmetry_on'),
        (1,'symmetry_on'),
        (2,'symmetry_on, efficient symmetrization'),
        (3,'symmetry_on, only forces and stress tensor')
    ])

class IchargTags(IncarBaseTags):
    tag_name = 'ICHARG'
    tag_dictionary = OrderedDict([
        (0,'Calculate charge density from initial wave functions.'),
        (1,'Read the charge density from file CHGCAR'),
        (2,'Take superposition of atomic charge densities')
    ])

class IsmearTags(IncarBaseTags):
    tag_name = 'ISMEAR'
    tag_dictionary = OrderedDict([
        (-5,'tetrahedron method with Blochl corrections'),
        (-4,'tetrahedron method'),
        (0,'method of Gaussian smearing'),
        (1,'method of Methfessel-Paxton order 1'),
        (2,'method of Methfessel-Paxton order 2')
    ])

class SigmaTag(IncarBaseFloatTag):
    tag_name = 'SIGMA'
    comment = 'width of the smearing in eV.'

class SymprecTag(IncarBaseFloatTag):
    tag_name = 'SYMPREC'
    comment = 'determines how accurate positions must be'


class NelmTag(IncarBaseIntegerTag):
    tag_name = 'NELM'
    comment = 'maximum number of electronic SCF steps'

    @classmethod
    def is_valid_option(cls, option):
        try:
            option_ = float(option)
        except ValueError:
            return False

        if option_ > 0:
            return True
        else:
            return False

class NelmdlTag(IncarBaseIntegerTag):
    tag_name = 'NELMDL'
    comment = "the number of non-selfconsistent steps at the beginning."

    @classmethod
    def is_valid_option(cls, option):
        try:
            option_ = int(option)
            return True
        except ValueError:
            return False


class NelminTag(IncarBaseIntegerTag):
    tag_name = "NELMIN"
    comment = 'minimum number of electronic SCF steps'

    @classmethod
    def is_valid_option(cls, option):
        try:
            option_ = float(option)
        except ValueError:
            return False

        if option_ > 0:
            return True
        else:
            return False

class PrecTags(IncarBaseTags):
    tag_name = 'PREC'
    tag_dictionary = OrderedDict([
        ('Accurate', 'avoid wrap around errors'),
        ('High', 'avoid wrap around errors')
    ])

class AlgoTags(IncarBaseTags):
    tag_name = 'ALGO'
    tag_dictionary = OrderedDict([
        ('Normal', 'blocked Davidson iteration scheme'),
        ('VeryFast', 'RMM-DIIS'),
        ('Fast', 'blocked Davidson, followed by RMM_DIIS')
    ])

class LchargTag(IncarBaseTags):
    tag_name = 'LCHARG'
    tag_dictionary = OrderedDict([
        ('.TRUE.', 'write CHGCR, write CHG'),
        ('.FALSE.', 'no CHGCAR, no CHG')
    ])

class LrealTags(IncarBaseEnumeratedTag):
    tag_name = 'LREAL'
    tag_dictionary = OrderedDict([
        ('.FALSE.', 'projection done in reciprocal space'),
        ('On', 'method of King-Smith, et al. Phys. Rev B 44, 13063 (1991).'),
        ('Auto', 'unpublished method of G. Kresse')
    ])

class LorbitTags(IncarBaseEnumeratedTag):
    tag_name = 'LORBIT'
    tag_dictionary = OrderedDict([
        (0, 'DOSCAR and PROCAR'),
        (1, 'DOSCAR and lm-decomposted PROCAR'),
        (2, 'DOSCAR, lm_decomposed PROCAR, phase factors'),
        (5, 'DOSCAR, PROCAR'),
        (10, 'DOSCAR, PROCAR'),
        (11, 'DOSCAR, lm-decomposed PROCAR'),
        (12, 'DOSCAR, lm-decomposed PROCAR, phase factors'),
    ])

class LplaneTag(IncarBaseEnumeratedTag):
    tag_name = 'LORBIT'
    tag_dictionary = OrderedDict([
        ('.TRUE.', 'use real space projectors, small number of compute nodes'),
        ('.FALSE.', 'no real space projectors, large number of compute nodes')
    ])

class LwaveTag(IncarBaseTags):
    tag_name = 'LWAVE'
    tag_dictionary = OrderedDict([
        ('.TRUE.', 'write WAVECAR'),
        ('.FALSE.', 'do not write WAVECAR')
    ])

class LvtotTag(IncarBaseTags):
    tag_name = 'LVTOT'
    tag_dictionary = OrderedDict([
        ('.TRUE.', 'write LOCPOT'),
        ('.FALSE.', 'no LOCPOT')
    ])

class NparTag(IncarBaseIntegerTag):
    tag_name = 'NPAR'
    comment = 'number of bands to be treated in parallel'
    
    @classmethod
    def is_valid_option(cls, option):
        if not isinstance(option, int):
            return False
        else:
            if option <= 0:
                return False
            else:
                return True

class NsimTag(IncarBaseIntegerTag):
    tag_name = 'NSIM'
    comment = 'number of bands to optimize simultaneously'
    
    @classmethod
    def is_valid_option(cls, option):
        if not isinstance(option, int):
            return False
        else:
            if option <= 0:
                return False
            else:
                return True
                
class IspinTags(IncarBaseTags):
    tag_name = 'ISPIN'
    tag_dictionary = OrderedDict([
        (1, 'non-spin polarized calculations'),
        (2, 'spin polarized calculations')
    ])

class IBrionTags(IncarBaseTags):
    tag_name = 'IBRION'
    tag_dictionary = OrderedDict([
        (0, 'molecular dynamics'),
        (1, 'ionic relaxation by RMM-DIIS'),
        (2, 'ionic relaxation by CG'),
        (3, 'ionic relaxation by damped MD'),
        (5, 'phonons, by frozen ion, without symmetry'),
        (6, 'phonons, by frozen ion, with symmetry'),
        (7, 'phonons, by perturbation theory, no symmetry'),
        (8, 'phonons, by perturbtion theory, with symmetry')
    ])

class IsifTag(IncarBaseEnumeratedTag):
    tag_name = 'ISIF'
    tag_dictionary = OrderedDict([
        (2, 'relaxation, ions=T, cellshape=F, cellvolume=F'),
        (3, 'relaxation, ions=T, cellshape=T, cellvolume=T'),
        (4, 'relaxation, ions=T, cellshape=T, cellvolume=F'),
        (5, 'relaxation, ions=F, cellshape=T, cellvolume=F'),
        (6, 'relaxation, ions=F, cellshape=T, cellvolume=T'),
        (7, 'relaxation, ions=F, cellshape=F, cellvolume=T')
    ])


class PotimTag(IncarBaseFloatTag):
    tag_name = 'POTIM'
    comment = 'scaling factor in relaxation'

class NswTag(IncarBaseFloatTag):
    tag_name = 'NSW'
    comment = 'maximum number of ionic relaxation steps'


class SystemTag(IncarBaseStringTag):
    tag_name = 'SYSTEM'


class IncarComments():
    tag_dictionary = {
        'ISTART':IstartTags,
        'ISYM':IsymTags,
        'SYMPREC':SymprecTag
    }

    @staticmethod
    def get_comment(tag_name, tag_option):
        return tag_dictionary[tag_name].get_comment(tag_option)

incar_tag_dictionary = {
    'ISTART':IstartTags
}