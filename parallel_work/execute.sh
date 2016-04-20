#!/bin/bash

#SBATCH --ntasks=8
#SBATCH --nodes=8
#SBATCH --tasks-per-node=1
#SBATCH --time=01:00:00 

#SBATCH --partition=training
#SBATCH --account=parallelcomputing

#SBATCH --job-name=mpi
#SBATCH --output="out/out_mpi8.txt"

module load java
module load openmpi/gcc

mpiexec ./prod-cons