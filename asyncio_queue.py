#!/usr/bin/env python
#
# Brief description:
# This sample simulates a pipeline of two worker pools take tasks from the queue and produce results concurrently.
# This is a thread-level concurrency sample program.
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

import asyncio
import time

class simulator:
    def __init__(self):
        
        self.number_of_input = 100
        
        self.pool_1_max_sleep = 0
        self.pool_1_min_sleep = 0
        self.pool_2_max_sleep = 5
        self.pool_2_min_sleep = 5

        self.pool_1_max = 10
        self.pool_2_max = 10
        self.pool_1_current = 0
        self.pool_2_current = 0

    async def power(self, tup):
        if tup[0] <= self.pool_1_max/2:
            await asyncio.sleep(self.pool_1_max_sleep)
        else:
            await asyncio.sleep(self.pool_1_min_sleep)
        return tup[0], tup[1]*tup[1]

    async def divide(self, tup):
        if tup[0] <= self.pool_2_max/2:
            await asyncio.sleep(self.pool_2_max_sleep)
        else:
            await asyncio.sleep(self.pool_2_min_sleep)
        return tup[0], tup[1]/2

    async def fill_input_que(self, n):
        for job in range(1, n+1):
            await self.input_que.put(job)
            print(f"put job {job} to input_que")

    async def pool_1_consumer(self, name):
        while True:
            job = await self.input_que.get()
            if job is None:
                break
            print(f"{name} got job {job} from input_que; input_que size: {self.input_que.qsize()}")
            self.pool_1_current = self.pool_1_current + 1
            # print(f"pool 1 current - {self.pool_1_current}")
            await self.wait_que.put(await self.power((job, job)))
            self.input_que.task_done()
    
    async def pool_2_consumer(self, name):
        while True:
            job = await self.wait_que.get()
            self.pool_1_current = self.pool_1_current - 1
            if job is None:
                break
            print(f"{name} got job {job[0]} from wait_que; wait_que size: {self.wait_que.qsize()}")
            self.pool_2_current = self.pool_2_current + 1
            # print(f"pool 2 current - {self.pool_2_current}")
            print(f"result: {await self.divide(job)}")
            self.pool_2_current = self.pool_2_current - 1
            # print(f"pool 2 current - {self.pool_2_current}")
            self.wait_que.task_done()                

    async def run(self):
        self.loop = asyncio.get_event_loop()
        self.input_que = asyncio.Queue(loop=self.loop)
        self.wait_que = asyncio.Queue(loop=self.loop)

        await sim.fill_input_que(self.number_of_input)

        tasks = []
        
        for i in range(self.pool_1_max):
            tasks.append(asyncio.create_task(self.pool_1_consumer(f"pool_1 worker-{i}")))

        for i in range(self.pool_2_max):
            tasks.append(asyncio.create_task(self.pool_2_consumer(f"pool_2 worker-{i}")))
        
        try:
            await self.input_que.join()
            await self.wait_que.join()
            for task in tasks:
                task.cancel()
        except KeyboardInterrupt:
            print("keyboard interrupted")
        finally:
            await asyncio.gather(*tasks, return_exceptions=True)
        
if __name__ == "__main__":
    import cProfile
    sim = simulator()
    cProfile.run("asyncio.run(sim.run(), debug=True)")
    
