#!/bin/bash

#SBATCH --ntasks=10
#SBATCH --nodes=10
#SBATCH --tasks-per-node=1
#SBATCH --time=02:00:00 

#SBATCH --partition=training
#SBATCH --account=parallelcomputing

#SBATCH --job-name=mpi
#SBATCH --output="out/out_mpi10.txt"

module load java
module load openmpi/gcc

mpiexec ./prod-cons