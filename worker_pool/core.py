#!/bin/env python3

# Python version: 3.9
# Author: Liam Ling
# Contact: liamlingdev@gmail.com
# File name: core.py
# Description:
""".
"""

import logging

from worker_1 import Worker_1
from worker_2 import Worker_2
from worker_pool_agent import WorkerPoolAgent

logger = logging.getLogger(__name__)

async def run():
    with WorkerPoolAgent(
        worker_1=Worker_1,
        worker_1_args=(
            ...
        ),
        worker_2=Worker_2,
        worker_2_args=(
            ...
        ),
    ) as worker_pool_agent:
        try:
            await worker_pool_agent.start()
        except KeyboardInterrupt:
            logger.debug("Ctrl+c caught, terminating...")
        except Exception as error:
            raise (error)
    return 0
