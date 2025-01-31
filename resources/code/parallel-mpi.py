import os
from mpi4py import MPI
from random import random

iterations : int = int(os.getenv("ITERATIONS", 10_000_000))

comm = MPI.COMM_WORLD

count : int = 0
for i in range(int(iterations / comm.size)):
    (x,y) = (random(), random())
    if x * x + y * y < 1.0:
        count += 1

sum_count = comm.reduce(count, MPI.SUM)

# Reducer style
if comm.rank == 0:
    print("Result:", (4.0 * int(sum_count) / iterations) )