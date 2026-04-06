import os
from mpi4py import MPI
import numpy as np
import random

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

start_message = 'hello world!'
end_message = 'goodbye world!'
data = []
    
if rank == 0:
    data.append(start_message)

    n = random.randrange(1, 10, 1)
    data.append(n)
    #print(data)
    comm.send(data, dest=rank+1)

if rank == 1:
    data = comm.recv(source=0)
    data.append(data[rank] * rank)
    #print(data)
    comm.send(data, dest=rank+1)
        
elif rank in range(2, 4):
    data = comm.recv(source=rank-1)
    data.append(data[rank] * rank)
    #print(data)
    comm.send(data, dest=rank+1)
    
elif rank == size-1: 
    data = comm.recv(source=3)
    data.append(data[rank] * rank)
    data.append(end_message)
    #print(data)
    comm.send(data, dest=0)

if rank == 0: 
    data = comm.recv(source=4)
    print(data)