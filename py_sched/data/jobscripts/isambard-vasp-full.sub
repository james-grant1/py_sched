#!/bin/bash --login
# Jobscript created with py_sched

# General job parameters
#PBS -N vasp_job

# Specify job resources
#PBS -l select=1
#PBS -l ncpus=64
#PBS -l walltime=10:0:0

# Specify accounting details 
#PBS -q arm

# Load modules for job
module swap PrgEnv-cray PrgEnv-gnu
module swap gcc/8.2.0 gcc/7.3.0

# Set number threads
export OMP_NUM_THREADS=1

# Move to directory that script was submitted from
cd $PBS_O_WORKDIR

# XC requires use of aprun to launch job on compute notes
aprun -n 64 -N 64 vasp_std 2>&1 > vasp_job.log
