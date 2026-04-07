#Import packages
import os
from mpi4py import MPI
import numpy as np
import random

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

start_message = 'hello world!' 
end_message = 'goodbye world!' 
data = [] #initialize empty data list
    
if rank == 0:
    data.append(start_message) #first item to be in data list

    n = random.randint(1, 10)
    data.append(n)
    #print(data)
    comm.send(data, dest=rank+1) 

if rank == 1:
    data = comm.recv(source=0)
    data.append(data[rank] * rank) #multiply random number n by 1
    #print(data)
    comm.send(data, dest=rank+1) 
        
elif rank in range(2, 4):
    data = comm.recv(source=rank-1)
    data.append(data[rank] * rank) #multiply last item in data list by rank
    #print(data)
    comm.send(data, dest=rank+1) 

elif rank == size-1: 
    data = comm.recv(source=3)
    data.append(data[rank] * rank) 
    data.append(end_message) #last item to be in data list
    #print(data)
    comm.send(data, dest=0)

if rank == 0: 
    data = comm.recv(source=4)
    print(data)