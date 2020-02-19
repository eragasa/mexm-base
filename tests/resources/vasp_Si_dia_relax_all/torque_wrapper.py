import os
import sys
import subprocess

def torque_submit_job(submission_script_path):

    cmd = ['qsub', submission_script_path]
    subprocess_result = subprocess.run(cmd, stdout=subprocess.PIPE)
    subprocess_stdout = subprocess_result.stdout.decode('utf-8')
    return subprocess_stdout

def torque_get_job_info_for_all_jobs(username=None):
    if username is None:
        username_ = os.environ['USER']
        if username_ is None:
            msg = "cannot resolve the username from environment variable"
            raise ValueError(msg)
    elif isinstance(username, str):
        username_ = username
    else:
        username_type = str(type(username_))
        msg = 'Invalid type {}, username must be a str or None'.format(username_type)
        raise TypeError(msg)
    cmd = ['qstat', '-u', username_]
    subprocess_result = subprocess.run(cmd, stdout=subprocess.PIPE)
    subprocess_stdout = subprocess_result.stdout.decode('utf-8')

    if subprocess_stdout == "":
        jobs_info = []
    else:
        jobs_info = []
        lines = subprocess_stdout.split('\n')
        
        is_task = False
        for line in lines:
            tokens = [k.strip() for k in line.split()]
            if len(tokens) > 0:
                if is_task:
                    jobs_info.append(list(tokens))
                if tokens[0].startswith('---'):
                    is_task = True

    return jobs_info

if __name__ == "__main__":
    if False:
        submission_script_path = "runjob_pitzer_debug.sh" 
        torque_job_id = torque_submit_job(submission_script_path=submission_script_path)
        print('torque_job_id:',torque_job_id)

    if True:
        torque_jobs_info = torque_get_job_info_for_all_jobs()
        print(torque_jobs_info)
 
