#!/bin/bash
#SBATCH --job-name="hello world!"
#SBATCH --output="%j_%x.out"
#SBATCH --partition=debug
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:00:05
srun echo "Hello"
srun echo "Nodes assigned: $SLURM_NODELIST"
srun echo "CPUs/node: $SLURM_CPUS_ON_NODE"
srun sleep 10
srun echo "World!"

