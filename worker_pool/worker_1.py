#!/bin/env python3

# Python version: 3.9
# Author: Liam Ling
# Contact: liamlingdev@gmail.com
# File name: worker_1.py
# Description:
"""
"""

import asyncio
from typing import Any, Callable, Tuple

from worker_base import WorkerBase


class Worker_1(WorkerBase):
    @classmethod
    def generate(
        cls,
        coro: Callable[..., Any] = None,
        asyncState: type = None,
        args: Tuple[Any, ...] = (),
        name: str = None,
    ):
        if coro is None:
            coro = cls._default_procedure
        return cls(
            coro=coro(
                *(
                    (
                        name,
                        asyncState,
                    )
                    + args
                )
            ),
            name=name,
        )

    @staticmethod
    async def _default_procedure(
        worker_name: str = "",
        asyncState: type = None):
        while True:
            Worker_1.step_1()
            if asyncState.total_processed is not None:
                asyncState.total_processed += 1
            await asyncio.sleep(0.001)

    @staticmethod
    async def step_1():
        pass
