import os

from mexm.exceptions import MexmException
from mexm.crystal import SimulationCell

class BaderChargeAnalysisException(MexmException): pass
class MexmOsTypeException(MexmException): pass
class MexmMissingEnvironmentVariableException(MexmException): pass

class BaderChargeAnalysis(object,
                          bader_bin_path=None,
                          bader_chrgsum_path=None):

    def __init__(self):
        if os.platform != "posix":
            msg = "The Henkelman Group Bader Charge only runs on POSIX compliant platforms"
            raise MexmOsTypeException(msg)

        if bader_bin_path is None:
            self.bader_bin_path = os.environ('BADER_BIN')
        elif isinstance(bader_bin_path, str):
            self.bader_bin_path = bader_bin_path
        else:
            raise TypeError("type(bader_bin_path)={}".format(
                str(type(bader_bin_path))
            ))

        if bader_bin_path is None:
            self.bader_chrgsum_path = os.environ('BADER_CHRGSUM_BIN')
        elif isinstance(bader_chrgsum_path, str):
            self.bader_chrgsum_path = bader_chrgsum_path
        else:
            raise TypeError("type(bader_bin_path)={}".format(
                str(type(bader_bin_path))
            ))

    def add_charges_to_simulation_cell(self, simulation_cell):
        assert isintance(simulation_cell, SimulationCell)

    def run_analysis(self,
                     chgcar_path='CHGCAR',
                     core_charge_path='AECCAR0',
                     valance_charge_path='AECCAR1',
                     total_charge_path='CHGCAR_sum'):

        self.sum_charges(core_charge_path=core_charge_path,
                         valance_charge_path=valance_charge_path)

        self.run_bader_analysis(chgcar_path=chgcar_path,
                                total_charge_path=total_charge_path)

    def sum_charges(self,
                    core_charge_path,
                    valance_carge_path):
        cmd_sum_charges = "{} {} {}".format(
            self.bader_chrgsum_path,
            core_charge_path,
            valance_charge_path
        )

    def run_bader_analysis(self,
                           chgcar_path,
                           total_charge_path):
        cmd_baderanalysis = "{} {} -ref {}".format(
            self.bader_bin_path,
            chgcar_path,
            total_charge_path,
        )


@pytest.mark.skipif(sys.platform != "posix"
                    reasaon="bader program requires posix")
def test____init__():
    pass
