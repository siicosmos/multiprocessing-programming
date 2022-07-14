#!/bin/env python3

# Python version: 3.9
# Author: Liam Ling
# Contact: liamlingdev@gmail.com
# File name: worker_pool_agent.py
# Description:
"""
"""

import asyncio
import logging
import threading
from typing import Any, Tuple

from config import config
from worker_base import WorkerBase

logger = logging.getLogger(__name__)


class WorkerPoolAgent:
    max_worker = int(config.max_worker)

    def __init__(self, worker_1: asyncio.Task = None, worker_1_args: Tuple[Any, ...] = None, worker_2: WorkerBase = None, worker_2_args: Tuple[Any, ...] = None) -> None:
        self.asyncState = type("", (), {})()
        self.asyncState.total_processed = 0
        self.asyncState.working = True
        self.worker_pool = []
        # initialize the pool when the instance gets created
        self.__initialize_worker_pool(worker_1, worker_1_args, worker_2, worker_2_args)

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb) -> None:
        self.join()

    def __initialize_worker_pool(
        self, worker_1: asyncio.Task = None, worker_1_args: Tuple[Any, ...] = None, worker_2: asyncio.Task = None, worker_2_args: Tuple[Any, ...] = None
    ) -> None:
        logger.debug(f"Worker_1 arguments passed in: {worker_1_args}")
        logger.debug(f"Worker_2 arguments passed in: {worker_2_args}")
        self.worker_pool.append(
            worker_1.generate(asyncState=self.asyncState, args=worker_1_args, name="Worker-1")
        )  # add timestamp check worker to the worker pool
        for i in range(1, self.max_worker + 1):
            self.worker_pool.append(
                worker_2.generate(
                    asyncState=self.asyncState, args=worker_2_args, name=f"Worker_2-{i}"
                )
            )

    async def start(self) -> None:
        for worker in self.worker_pool:
            logger.debug(f"Worker created: {worker}")
        self.results = await asyncio.gather(*self.worker_pool, return_exceptions=False)

    def join(self) -> None:
        self.__Joiner(worker_pool=self.worker_pool).start()

    class __Joiner(threading.Thread):
        def __init__(self, worker_pool: list[asyncio.Task] = None):
            threading.Thread.__init__(self)
            self.worker_pool = worker_pool

        def run(self):
            self.__start_joining()

        def __start_joining(self) -> None:
            try:
                for worker in self.worker_pool:
                    logger.debug(f"{worker.get_name()} start joining")
                    worker.cancel()
                    logger.debug(f"{worker.get_name()} canceled")
            except Exception as error:
                logger.error(f"{error}")
