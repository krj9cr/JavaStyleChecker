#!/bin/bash


module load openmpi/gcc

# Re-compile the program
mpicc -O3 prod-cons.c -o prod-cons

# Submit job
sbatch execute.sh
