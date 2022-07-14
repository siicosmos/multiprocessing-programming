#!/bin/env python3

# Python version: 3.9
# Author: Liam Ling
# Contact: liamlingdev@gmail.com
# File name: __main__.py
# Description:
"""This invokes the main function.
"""

import sys
import asyncio
import logging

from . import core

logger = logging.getLogger(__name__)

def main():
    try:
        return asyncio.run(core.run())
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    sys.exit(main())
