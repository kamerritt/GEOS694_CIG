#Import packages
import os
from mpi4py import MPI
import numpy as np
import random

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

n = random.randint(1, 1000) #generate random integer for each rank

max = comm.reduce(n, op=MPI.MAX, root=0) #global max across all ranks

max = comm.bcast(max, root=0) #broadcast global max from root 0 to all ranks

#print statement if a root's random number is the global max
if n == max:
    print(f'Rank {rank} has value {n} which is the global max {max}')

#print statement if a root's random number is less than the global max
else:
    print(f'Rank {rank} has value {n} which is less than the global max {max}')
