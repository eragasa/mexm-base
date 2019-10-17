""" module to manage jobs to slurm """
import os, yaml
from copy import copy, deepcopy
from collections import OrderedDict

from mexm.io.filesystem import OrderedDictYAMLLoader

class SlurmConfiguration():
    """
    Args:
        path(str): path to the YAML formatted configuration filew
    Raises:
        KeyError: if the MEXM_SLURM_CONFIG_PATH is not setWhen the path argument is not specified then, the path
            will be retrieved from MEXM_SLURM_CONIG_PATH,
    """

    def __init__(self, path=None):
        self.configuration = OrderedDict()

        if path is not None:
            self.read(path=path)

    @staticmethod
    def initailize_from_dict(obj_dict):
        """ factory method which initializes and object from a dict """
        obj_slurm = SlurmConfiguration()
        obj_slurm.__configure_from_dict(obj_dict=obj_dict)
        return obj_slurm

    def read(self, path):
        with open(path, 'r') as f:
            obj_dict = yaml.load(f, OrderedDictYAMLLoader)
            self.configure_from_dict(obj_dict=obj_dict)

    def write(self,path):
        with open(path, 'w') as f:
            yaml_str = yaml.dump(self.to_dict(),
                                 default_flow_style=False
                                 )
            f.write(yaml_str)

    def to_dict(self):
        return self.configuration

    def configure_from_dict(self, obj_dict):
        assert isinstance(obj_dict, dict)

        self.configuration = deepcopy(obj_dict)

    @property
    def slurm_configuration(self):
        return self.configuration['slurm']

    @property
    def lammps_configuration(self):
        return self.configuration['lammps']

    @property
    def vasp_configuration(self):
        return self.configuration['vasp']

    @property
    def phonts_configuration(self):
        return self.configuration['phonts']

    def set_slurm_configuration(self,
                                job_name,
                                qos,
                                mail_type,
                                mail_name,
                                ntasks,
                                output_path,
                                error_path,
                                time,
                                memory):
        self.configuration['slurm'] = OrderedDict([
            ('job_name',job_name),
            ('qos', qos),
            ('mail_type', mail_type),
            ('mail_name', mail_name),
            ('ntasks', ntasks),
            ('output_path', output_path),
            ('error_path', error_path),
            ('time', time),
            ('memory', memory)
        ])

    def set_vasp_configuration(self,
                               modules,
                               run_string):
        self.configuration['vasp'] = OrderedDict([
            ('modules', deepcopy(modules)),
            ('run_string', run_string)
        ])

    def set_phonts_configuration(self,
                                 modules,
                                 run_string):
        self.configuration['phonts'] = OrderedDict([
            ('modules', deepcopy(modules)),
            ('run_string', run_string)
        ])

    def set_lammps_configuration(self,
                                 modules,
                                 run_string):
        self.configuration['lammps'] = OrderedDict([
            ('modules', deepcopy(modules)),
            ('run_string', run_string)
        ])

class SlurmSubmissionScript(object):

    def __init__(self, sonfiguration=None):
        if configuration is None:
            path_ = os.environ('MEXM_SLURM_CONFIG_PATH')
            self.configuration = SlurmConfiguration(path=path_)
        elif isinstance(slurm_configuration, str):
            path_ = configuration
            self.configuration = SlurmConfiguration(path=path_)
        elif isinstance(configuration, OrderedDict):
            self.configuration = SlurmConfiguration.initailize_from_dict(
                    obj_dict=slurm_configuration
            )
        elif slurm_configuration == 'empty':
            self.configuration = SlurmConfiguration

    @property
    def slurm_configuration(self):
        return self.configuration.slurm_configuration

    def section_header_section_to_str(self):
        job_name_ = self.slurm_configuration['job_name']
        qos_ = self.slurm_configuration['qos']
        mail_type = self.slurm_configuration['mail_type']
        mail_name = self.slurm_configuration['mail_name']
        ntasks_ = self.slurm_configuration['ntasks']
        time_ = self.configuration['time']
        output_path_ = self.configuration['output_path']
        error_path_ = self.configuration['error_path']
        memory_ = self.configuration['memory']

        str_out = '#!/bin/bash\n'
        str_out += '#SBATCH --job-name={}\n'.format(job_name_)
        str_out += '#SBATCH --qos={}\n'.format(qos_)
        str_out += '#SBATCH --mail-type={}\n'.format(mail_type_)
        str_out += '#SBATCH --mail-user={}\n'.format(mail_name)
        str_out += '#SBATCH --ntasks={}\n'.format(ntasks_)
        str_out += '#SBATCH --distribution=cyclic:cyclic\n'
        str_out += '#SBATCH --mem={}\n'.format(memory_)
        str_out += '#SBATCH --time={}\n'.format(time_)
        str_out += '#SBATCH --output={}\n'.format(output_path_)
        str_out += '#SBATCH --error={}\n'.format(error_path_)

        return str_out

    def section_load_modules_to_str(self, modules=None):

        # since modules argument is specified, replace modules entry
        if modules is not None:
            self.configuration['modules'] = list(modules)
        modules_ = self.configuration['modules']

        str_out = ""
        for module in modules_:
            str_out += "module load {}\n".format(module)

        return str_out

    def section_slurm_debug_to_str(self):
        str_out = "\n".join([
            'echo slurm_job_id:$SLURM_JOB_ID'
            'echo slurm_job_name:$SLURM_JOB_NAME'
            'echo slurm_job_nodelist:$SLURM_JOB_NODELIST'
            'echo slurm_job_num_nodes:$SLURM_JOB_NUM_NODES'
            'echo slurm_cpus_on_node:$SLURM_CPUS_ON_NODE'
            'echo slurm_ntasks:$SLURM_NTASKS'
            'echo working directory:$(pwd)'
            'echo hostname:$(hostname)'
            'echo start_time:$(date)'
        ]) + "\n"
        return str_out

    def section_postprocessing_to_str(self):
        str_out = "touch jobComplete\n"
        str_out += "echo end_time:$(date)\n"
        return str_out


class SlurmSubmissionScript(object):

    def __init__(self,slurm_dict=None):
        if slurm_dict is None:
            self.configuration = OrderedDict()
        else:
            assert isinstance(slurm_dict,dict)
            self.process_configuration_dictionary(slurm_dict)

    @property
    def slurm_configuration(self):
        return self.configuration.slurm_configuration

    def section_header_section_to_str(self):
        job_name_ = self.slurm_configuration['job_name']
        qos_ = self.slurm_configuration['qos']
        mail_type = self.slurm_configuration['mail_type']
        mail_name = self.slurm_configuration['mail_name']
        ntasks_ = self.slurm_configuration['ntasks']
        time_ = self.configuration['time']
        output_path_ = self.configuration['output_path']
        error_path_ = self.configuration['error_path']
        memory_ = self.configuration['memory']

        str_out = '#!/bin/bash\n'
        str_out += '#SBATCH --job-name={}\n'.format(job_name_)
        str_out += '#SBATCH --qos={}\n'.format(qos_)
        str_out += '#SBATCH --mail-type={}\n'.format(mail_type_)
        str_out += '#SBATCH --mail-user={}\n'.format(mail_name)
        str_out += '#SBATCH --ntasks={}\n'.format(ntasks_)
        str_out += '#SBATCH --distribution=cyclic:cyclic\n'
        str_out += '#SBATCH --mem={}\n'.format(memory_)
        str_out += '#SBATCH --time={}\n'.format(time_)
        str_out += '#SBATCH --output={}\n'.format(output_path_)
        str_out += '#SBATCH --error={}\n'.format(error_path_)

        return str_out

    def section_load_modules_to_str(self, modules=None):

        # since modules argument is specified, replace modules entry
        if modules is not None:
            self.configuration['modules'] = list(modules)
        modules_ = self.configuration['modules']

        str_out = ""
        for module in modules_:
            str_out += "module load {}\n".format(module)

        return str_out

    def section_slurm_debug_to_str(self):
        str_out = "\n".join([
            'echo slurm_job_id:$SLURM_JOB_ID'
            'echo slurm_job_name:$SLURM_JOB_NAME'
            'echo slurm_job_nodelist:$SLURM_JOB_NODELIST'
            'echo slurm_job_num_nodes:$SLURM_JOB_NUM_NODES'
            'echo slurm_cpus_on_node:$SLURM_CPUS_ON_NODE'
            'echo slurm_ntasks:$SLURM_NTASKS'
            'echo working directory:$(pwd)'
            'echo hostname:$(hostname)'
            'echo start_time:$(date)'
        ]) + "\n"
        return str_out

    def section_command_to_str(self,command=None):
        if command is not None:
            self.configuration['command'] = command
        command_ = self.configuration['command']

        if isinstance(command_, str):
            str_out = command_
        elif isinstance(command_, list):
            str_out = "\n".join(command_) + "\n"
        else:
            raise TypeError()

        return str_out

    def section_postprocessing_to_str(self):
        str_out = "touch jobComplete\n"
        str_out += "echo end_time:$(date)\n"
        return str_out

    def slurm_script_string(self):
        str_out = self.section_header_section_to_str()
        str_out += "#<---------- SLURM debug information"
        str_out += self.section_slurm_debug_to_str()
        str_out += '#<---------- load necessary modules\n'
        str_out += '#<---------- run application\n'
        str_out += self.section_command_to_str()
        str_out += '#<---------- post-processing steps'
        str_out += section_postprocessing_to_str()
        return str_out

    def write(self, path='runjob.slurm',job_name=None):
        self.filename=filename
        if job_name is not None:
            self.configuration['job_name'] = job_name

        str_out = self.slurm_script_string(self)
        with open(filename,'w') as f:
            f.write(str_out)

def write_phonts_batch_script(filename,job_name,email,qos,ntasks,time,
        output='job.out',error='job.err'):
    s = '#!/bin/bash\n'
    s += '#SBATCH --job-name={}\n'.format(job_name)
    s += '#SBATCH --qos={}\n'.format(qos)
    s += '#SBATCH --mail-type=END\n'
    s += '#SBATCH --mail-user={}\n'.format(email)
    s += '#SBATCH --ntasks={}\n'.format(ntasks)
    s += '#SBATCH --distribution=cyclic:cyclic\n'
    s += '#SBATCH --time={}\n'.format(time)
    s += '#SBATCH --output={}\n'.format(output)
    s += '#SBATCH --error={}\n'.format(error)


    s += 'echo slurm_job_id:$SLURM_JOB_ID\n'
    s += 'echo slurm_job_name:$SLURM_JOB_NAME\n'
    s += 'echo slurm_job_nodelist:$SLURM_JOB_NODELIST\n'
    s += 'echo slurm_job_num_nodes:$SLURM_JOB_NUM_NODES\n'
    s += 'echo slurm_cpus_on_node:$SLURM_CPUS_ON_NODE\n'
    s += 'echo slurm_ntasks:$SLURM_NTASKS\n'

    s += 'echo working directory:$(pwd)\n'
    s += 'echo hostname:$(hostname)\n'
    s += 'echo start_time:$(date)\n'

    s += 'module load intel openmpi\n'
    s += '\n'
    s += 'srun --mpi=pmi2 $PHONTS_BIN > phonts.log\n'
    s += 'touch jobCompleted\n'
    s += 'echo end_time:$(date)\n'

    with open(filename,'w') as f:
        f.write(s)

def write_vasp_batch_script(filename,job_name,email,qos,ntasks,time,
        output='job.out',
        error='job.err',
        vasp_bin=None):

    intel_compiler_string = ""
    mpi_compiler_string = ""

    if vasp_bin is None:
        _vasp_bin = os.environ['VASP_BIN']
    else:
        _vasp_bin = vasp_bin

    s = '#!/bin/bash\n'
    s += '#SBATCH --job-name={}\n'.format(job_name)
    s += '#SBATCH --qos={}\n'.format(qos)
    s += '#SBATCH --mail-type=END\n'
    s += '#SBATCH --mail-user={}\n'.format(email)
    s += '#SBATCH --ntasks={}\n'.format(ntasks)
    s += '#SBATCH --distribution=cyclic:cyclic\n'
    s += '#SBATCH --time={}\n'.format(time)
    s += '#SBATCH --output={}\n'.format(output)
    s += '#SBATCH --error={}\n'.format(error)

    if vasp_bin is not None:
        s += "VASP_BIN={}\n".format(_vasp_bin)
        s += "export VASP_BIN"

    s += 'echo slurm_job_id:$SLURM_JOB_ID\n'
    s += 'echo slurm_job_name:$SLURM_JOB_NAME\n'
    s += 'echo slurm_job_nodelist:$SLURM_JOB_NODELIST\n'
    s += 'echo slurm_job_num_nodes:$SLURM_JOB_NUM_NODES\n'
    s += 'echo slurm_cpus_on_node:$SLURM_CPUS_ON_NODE\n'
    s += 'echo slurm_ntasks:$SLURM_NTASKS\n'

    s += 'echo working directory:$(pwd)\n'
    s += 'echo hostname:$(hostname)\n'
    s += 'echo start_time:$(date)\n'

    s += 'module load intel/2016.0.109\n'
    s += 'module load impi\n'
    s += 'srun --mpi=pmi2 $VASP_BIN > vasp.log\n'
    s += 'echo end_time:$(date)\n'

    with open(filename,'w') as f:
        f.write(s)

    @classmethod
    def load_module_string(cls):
        module_load_strings = ['module load {}'.format(k) for k in cls.modules]
        return "\n".join(module_load_strings)

    @classmethod
    def application_run_string(cls):
        return cls.application_run_string() + "\n"

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
