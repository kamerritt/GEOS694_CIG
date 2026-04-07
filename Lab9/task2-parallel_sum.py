#Import packages
import os
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
num_data = 1000 #number of data points 
data = None
    
if rank == 0:
    data = np.arange(1, num_data+1) 
    #print(data)
    partial = np.array_split(data, size) #divide data list into equal parts
    #print(partial)
else:
    partial = None 
    
part = comm.scatter(partial, root=0) #scatter partials among ranks

partial = sum(part) #compute the sum of the partial arrays of each rank
print('Partial sum = ', partial)

tot = comm.gather(partial, root=0) #bring sums together at rank 0

if rank == 0:
    overall_sum = sum(tot) #compute the total sum of all partial sums
    print('Total sum = ', overall_sum)