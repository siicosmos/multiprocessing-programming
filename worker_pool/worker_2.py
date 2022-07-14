#!/bin/env python3

# Python version: 3.9
# Author: Liam Ling
# Contact: liamlingdev@gmail.com
# File name: worker_2.py
# Description:
"""
"""

import asyncio
from typing import Any, Callable, Tuple

from worker_base import WorkerBase

sleep_frequency = 10

class Worker_2(WorkerBase):
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
        while asyncState.working:
            ... # do something
            await asyncio.sleep(sleep_frequency)
