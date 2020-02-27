import os
import subprocess

cmd = 'qstat -u {user}'.format(os.environ['USER'])
path = os.path.join(
    'resource',
    'qstat_stdout_results.txt'
)
with open(path) as f:
    lines = f.readlines()

n_lines = len(lines)
names = [k.strip().lower() for k in lines[0].split()]
print(names)


class TorqueJobSubmissionManager():

    def submit_job(
        self, 
        simulation_path: str,
        submission_script_path: str
    ):
        # setting an initial context, so I can return to it
        initial_path = os.pwd()

        os.chdir(simulation_path)
        cmd = ['qsub', submission_script_path]
        subprocess_result = subprocess.run(
            cmd, 
            stdout=subprocess.PIPE)
        subprocess_stdout = subprocess_result.stdout.decode('utf-8')
        
        # return to the original context
        os.chdir(initial_path)

        # return the results
        return subprocess_stdout

    def get_job_info(
        self,
        jobid='all', 
        username=None
    ):
        if username is None:
            username = os.environ['USER']
        else:
            username_ = username

        jobs_info = self.get_job_info_for_all_jobs(username=username_)
        return jobs_info


    def get_job_info_for_all_jobs(
        self,
        username: str
    ):
        cmd = ['qstat', '-u', username]
        subprocess_result = subprocess.run(
            cmd, 
            stdout=subprocess.PIPE
        )
        subprocess_stdout = subprocess_result.stdout.decode('utf-8')

        if subprocess_stdout == "":
            jobs_info = []
        else:
            jobs_info = {}
            for i_line in range(2, n_lines):
                tokens = [k.strip() for k in lines[i_line].split()]
                for i, v in enumerate(tokens):
                    print(i,v)
                jobid = tokens[0].split('.')[0]
                jobs_info[jobid] = {
                    'jobid':tokens[0],
                    'username':tokens[2],
                    'jobname':tokens[3],
                    'jobstatus':tokens[9]
                }
            print(jobs_info)

        return jobs_info

    def convert_jobstatus_to_string(char_jobstatus):
        char_to_jobstatus = {

            'C': 'complete'
        }
        