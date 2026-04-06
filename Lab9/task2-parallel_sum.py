import os
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
num_data = 1000
data = None
    
if rank == 0:
    data = np.arange(1, num_data+1)
    #print(data)
    partial = np.array_split(data, size)
    #print(partial)
else:
    partial = None 
    
part = comm.scatter(partial, root=0)

partial = sum(part)
print('Partial sum = ', partial)

tot = comm.gather(partial, root=0)

if rank == 0:
    overall_sum = sum(tot)
    print('Total sum = ', overall_sum)