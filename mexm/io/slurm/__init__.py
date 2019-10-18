""" module to manage jobs to slurm """
import os, yaml
from copy import copy, deepcopy
from collections import OrderedDict

from mexm.io.slurm.configuration import SlurmConfiguration
from mexm.io.slurm.submissionscript import SlurmSubmissionScript

class VaspSubmissionScript(SlurmSubmissionScript):

    def __init__(self, path=None):
        SlurmSubmissionScript.__init__(self, path)

    def slurm_section_to_string(self):
        job_name = self.job_name
        qos_name = self.qos_name
        mail_type = self.mail_type
        mail_user = self.mail_user
        ntasks = self.ntasks
        distribution = self.distribution
        time = self.time
        output = self.output_path
        error = self.error_path

        return_str = '#!/bin/bash\n'
        return_str += '#SBATCH --job-name={}\n'.format(job_name)
        return_str += '#SBATCH --qos={}\n'.format(qos_name)
        return_str += '#SBATCH --mail-type={}\n'.format(mail_type)
        return_str += '#SBATCH --mail-user={}\n'.format(mail_user)
        return_str += '#SBATCH --ntasks={}\n'.format(ntasks)
        return_str += '#SBATCH --distribution=cyclic:cyclic\n'
        return_str += '#SBATCH --time={}\n'.format(time)
        return_str += '#SBATCH --output={}\n'.format(output)
        return_str += '#SBATCH --error={}\n'.format(error)

        return return_str
    def write(self, path):
        self.slurm_section_to_string()
