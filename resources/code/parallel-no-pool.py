import time
import multiprocessing
from multiprocessing import Process, Manager
import os
from math import floor
from statistics import stdev
from random import Random

samples : int = int(os.getenv("SAMPLES", 5))
iterations : int = int(os.getenv("ITERATIONS", 10_000_000))
parallelization_coefficients : list[float] = [0.25, 0.5, 1]
logical_cores : int = multiprocessing.cpu_count()

assert samples > 0
assert iterations > 0

def partitioned_work(worker_index: int, workload: int, return_dict: list[int]):
    count = 0
    
    local_random = Random()
    local_random.seed(os.getpid())
    
    for _ in range(workload):
        (x,y) = (local_random.random(), local_random.random())
        if x * x + y * y < 1.0:
            count += 1
    
    return_dict[worker_index] = count

def wait_join_all(processes: list[Process]):
    for p in processes:
        p.join()

def calc_pi(max_processes: int, iterations: int):
    workload : int = floor(iterations / float(max_processes)) + 1
    
    processes : list[Process] = []
    total_inside : int = 0
    with Manager() as manager:
        return_dict = manager.dict()
        
        for idx in range(max_processes):
            p = Process(target=partitioned_work, args=(idx,workload, return_dict))
            p.start()
            processes.append(p)
        
        wait_join_all(processes)
        
        total_inside = sum(map(int, return_dict.values()))
    
    return 4.0 * total_inside / float(iterations)

if __name__ == '__main__':
    result = 0.0
    all_run_times : list[list[float]] = []
    for parallelization_coefficient in parallelization_coefficients:
        times : list[float] = []
        max_processes : int = floor(parallelization_coefficient * logical_cores)
        print('Doing ', samples, ' runs')
        print('Each with ', iterations, ' iterations')
        print('With ', max_processes, ' computation units')
        # print('Seeding random with ', ext_seed)
        for i in range(samples):
            print('\t Starting iteration', i)
            start_time = time.time()

            result = calc_pi(max_processes, iterations)

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
        all_run_times.append(times)
    
    print(all_run_times)