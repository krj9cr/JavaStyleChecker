#!/bin/bash

#SBATCH --ntasks=60
#SBATCH --nodes=3
#SBATCH --tasks-per-node=20
#SBATCH --time=02:00:00 

#SBATCH --partition=training
#SBATCH --account=parallelcomputing
#SBATCH --exclusive

#SBATCH --job-name=wow
#SBATCH --output="out/out_mpi60_for_0-1000_sun_script.txt"

module load java
module load openmpi/gcc

mpiexec ./prod-cons