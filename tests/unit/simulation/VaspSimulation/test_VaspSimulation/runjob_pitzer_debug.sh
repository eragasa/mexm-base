#PBS -A PAA0028
#PBS -l walltime=01:00:00
#PBS -l nodes=1:ppn=40 -q debug
#PBS -N si_job_name
#PBS -e job.err
#PBS -o job.out
#PBS -S /bin/bash


echo "The current working directory is $(pwd)"
echo "Switching to the working directory $PBS_O_WORKDIR" 
cd $PBS_O_WORKDIR

echo "switching compiler chain"
echo "module load intel/19.0.5"
module load intel/19.0.5
echo "module load intelmpi/2019.3"
module load intelmpi/2019.3

echo "VASP_STD_BIN=$VASP_STD_BIN"
mpiexec $VASP_STD_BIN

