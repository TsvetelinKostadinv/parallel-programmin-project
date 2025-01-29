import time
import os
from statistics import stdev
from random import random, seed

times : list[float] = []
samples : int = int(os.getenv("SAMPLES", 5))
iterations : int = int(os.getenv("ITERATIONS", 1_000_000))
ext_seed : int = int(os.getenv("SEED", 0xdeadbeef))
result : float = 0.0

def calc_pi(iterations: int):
    count = 0
    for _ in range(iterations):
        (x,y) = (random(), random())
        count += (x * x + y * y < 1.0)
    return 4.0 * float(count) / float(iterations)

assert samples > 0
assert iterations > 0
seed(ext_seed)

print('Doing ', samples, ' runs')
print('Each with ', iterations, ' iterations')
print('Seeding random with ', ext_seed)
for i in range(samples):
    print('\t Starting iteration', i)
    start_time = time.time()

    result = calc_pi(iterations)

    end_time = time.time()
    print('\t Stopped iteration', i)

    elapsed_time = end_time - start_time
    print('\t Elapsed time', elapsed_time)
    print('=' * 32)
    times.append(elapsed_time)

print("Final Results: ")
print("Calculated value: ", result)
print('Times: ', times)
print('Max: ', max(times))
print('Min: ', min(times))
print('Avg: ', sum(times) / len(times))
print('Sigma: ', stdev(times))