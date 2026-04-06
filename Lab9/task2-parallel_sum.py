import os
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
reduced = None
    
if rank == 0:
    data = np.arange(1, 20)

partial = np.empty(len(data)/size, dtype='d')
comm.Scatter(data, partial, root=0)

if rank in range(2, 5):
    partial = sum(partial)

comm.Gather(sum(partial), reduced, root=0)