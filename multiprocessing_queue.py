#!/usr/bin/env python
#
# Brief description:
# This sample simulates a pipeline of two worker pools take tasks from the queue and produce results concurrently.
# This is a process-level concurrency sample program.
#
# How it works:
# The input of the tasks will go into the input queue (aka input_que). Workers from pool 1 will take inputs from the input queue.
# Then workers from pool 1 will put the result into the wait queue (aka wait_que).
# Workers from pool 2 will get whatever in the wait queue and process it and generate results
#
# Test it out:
# Modify the variables in simulator class:
#   * number_of_input - define the number of tasks need to process
#   * pool_{n}_max_sleep - define maximum sleep time for workers in the pool {n} 
#   * pool_{n}_min_sleep - define minimum sleep time for workers in the pool {n} 
#   * pool_{n}_max - define maximum number of workers in the pool {n}
#   * pool_{n}_min - define minimum number of workers in the pool {n}
#   * pool_{n}_current - track the number of workers in the pool {n}
#
# Some conclusion from experiments:
# The different sizes of the worker pool and task elapsed time will create a bottleneck on the corresponding level of the pipeline.
# So the final time of finishing how the procedure will be added by the largest time needed for each batch*number of the possible largest batch for each level.
#
# Contact: lllcosmoslll@hotmail.com

import multiprocessing
import time

class simulator:
    def __init__(self):

        self.number_of_input = 10
        
        self.pool_1_max_sleep = 3
        self.pool_1_min_sleep = 3
        self.pool_2_max_sleep = 5
        self.pool_2_min_sleep = 5

        self.pool_1_max = 10
        self.pool_2_max = 10
        self.pool_1_current = 0
        self.pool_2_current = 0

        self.total_count = multiprocessing.Value("i",0)

    def power(self, tup):
        if tup[0] <= self.pool_1_max/2:
            time.sleep(self.pool_1_max_sleep)
        else:
            time.sleep(self.pool_1_min_sleep)
        return tup[0], tup[1]*tup[1]

    def divide(self, tup):
        if tup[0] <= self.pool_2_max/2:
            time.sleep(self.pool_2_max_sleep)
        else:
            time.sleep(self.pool_2_min_sleep)
        return tup[0], tup[1]/2

    def fill_input_que(self, n):
        for job in range(1, n+1):
            self.input_que.put(job)
            with self.total_count.get_lock():
                self.total_count.value += 1
            print(f"put job {job} to input_que")

    def pool_1_consumer(self, name):
        print(f"total proceed: {self.total_count.value}")
        while True:
            if self.input_que.empty():
                break
            job = self.input_que.get()
            print(f"{name} got job {job} from input_que; input_que size: {self.input_que.qsize()}")
            self.pool_1_current = self.pool_1_current + 1
            # print(f"pool 1 current - {self.pool_1_current}")
            self.wait_que.put(self.power((job, job)))
            self.input_que.task_done()
        print(f"{name} exited")
    
    def pool_2_consumer(self, name):
        print(f"total proceed: {self.total_count.value}")
        while True:
            if self.wait_que.empty() and self.total_count.value == 0:
                break
            job = self.wait_que.get()
            with self.total_count.get_lock():
                self.total_count.value -= 1
            self.pool_1_current = self.pool_1_current - 1
            print(f"{name} got job {job[0]} from wait_que; wait_que size: {self.wait_que.qsize()}")
            self.pool_2_current = self.pool_2_current + 1
            # print(f"pool 2 current - {self.pool_2_current}")
            print(f"result: {self.divide(job)}")
            print(f"total proceed: {self.total_count.value}")
            self.pool_2_current = self.pool_2_current - 1
            # print(f"pool 2 current - {self.pool_2_current}")
            self.wait_que.task_done()
        print(f"{name} exited")

    def run(self):

        self.input_que = multiprocessing.JoinableQueue()
        self.wait_que = multiprocessing.JoinableQueue()

        self.fill_input_que(self.number_of_input)

        pool_1_workers = []
        pool_2_workers = []
        
        for i in range(self.pool_1_max):
            pool_1_workers.append(multiprocessing.Process(target=self.pool_1_consumer, args=(f"pool_1 worker-{i}",)))
            pool_1_workers[i].start()

        for i in range(self.pool_2_max):
            pool_2_workers.append(multiprocessing.Process(target=self.pool_2_consumer, args=(f"pool_2 worker-{i}",)))
            pool_2_workers[i].start()
        
        try:
            self.input_que.join()
            self.wait_que.join()
            for worker in pool_1_workers:
                worker.join()
            for worker in pool_2_workers:
                worker.join()

        except KeyboardInterrupt:
            print("keyboard interrupted")
        finally:
            print("done")

        
if __name__ == "__main__":
    import cProfile
    sim = simulator()
    cProfile.run("sim.run()")
    
