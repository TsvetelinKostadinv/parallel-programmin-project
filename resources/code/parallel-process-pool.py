import time
import multiprocessing
from multiprocessing import Pool
import os
from statistics import stdev
from random import Random
from itertools import repeat

samples : int = int(os.getenv("SAMPLES", 5))
workload : int = int(os.getenv("WORKLOAD", 100_000))
num_workers : int = int(os.getenv("NUM_WORKERS", 10))
logical_cores : int = multiprocessing.cpu_count()

assert workload > 0
assert num_workers > 0
assert samples > 0

def partitioned_work(workload: int):
    count : int = 0
    
    local_random = Random()
    local_random.seed(os.getpid())
    
    for _ in range(workload):
        (x,y) = (local_random.random(), local_random.random())
        if x * x + y * y < 1.0:
            count += 1
    
    return count

def calc_pi():
    
    res : list[int] = []
    
    with Pool(processes = num_workers) as pool:
        res = pool.map(partitioned_work, repeat(workload, num_workers))
    
    total_inside = sum(res)
    
    return 4.0 * total_inside / float(workload * num_workers)

if __name__ == '__main__':
    times : list[float] = []
    print('Doing ', samples, ' runs')
    print('Each with ', workload * num_workers, ' iterations')
    print('With ', logical_cores, ' computation units')
    for i in range(samples):
        result = 0.0
        print('\t Starting iteration', i)
        start_time = time.time()

        result = calc_pi()

        end_time = time.time()
        print('\t Stopped iteration', i)

        elapsed_time = end_time - start_time
        print('\t Elapsed time: ', elapsed_time)
        print('\t Calculated result:', result)
        print('=' * 32)
        times.append(elapsed_time)
    print('=' * 32)
    print('=' * 32)

    print("Final Results: ")
    print('Times: ', times)
    print('Max: ', max(times))
    print('Min: ', min(times))
    print('Avg: ', sum(times) / len(times))
    print('Sigma: ', stdev(times))
