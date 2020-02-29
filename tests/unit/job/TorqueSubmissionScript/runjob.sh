#PBS -A PAA0028
#PBS -l walltime=72:00:00
#PBS -l nodes=1:ppn=40
#PBS -N Si_job_name
#PBS -e job.err
#PBS -o job.out
#PBS -S /bin/bash

cd $PBS_O_WORKDIR


module load intel/19.0.5
module load intelmpi/2019.3


mpiexec $VASP_STD_BIN > vasp.out