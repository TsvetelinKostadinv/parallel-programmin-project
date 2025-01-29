import time
from statistics import stdev
from random import random

def calc_pi(iterations: int):
    count = 0
    for _ in range(iterations):
        (x,y) = (random(), random())
        count += (x * x + y * y < 1.0)

times : list = []
samples : int = 5
iterations : int = 100_000_000

assert samples != 0

for i in range(samples):
    print('Starting iteration', i)
    start_time = time.time()

    calc_pi(iterations)

    end_time = time.time()
    print('Stopped iteration', i)

    elapsed_time = end_time - start_time
    print('Elapsed time', elapsed_time)
    times.append(elapsed_time)

print("Final Results: ")
print('Times: ', times)
print('Max: ', max(times))
print('Min: ', min(times))
print('Avg: ', sum(times) / len(times))
print('Sigma: ', stdev(times))