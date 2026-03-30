#!/bin/bash

#SBATCH --job-name=lumen_concerts_job
#SBATCH --output=/import/c1/GEOS694/kamerritt/GEOS694_ICG_KM/HW8/lumen_concerts_%j.outr
#SBATCH --partition=debug
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4

set -x

PYTHON=/home/kamerritt/miniforge3/envs/GEOS694/bin/python

cd /import/c1/GEOS694/kamerritt/GEOS694_ICG_KM/HW8

$PYTHON ./lumen_concerts.py
