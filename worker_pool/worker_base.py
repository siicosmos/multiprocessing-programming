#!/bin/env python3

# Python version: 3.9
# Author: Liam Ling
# Contact: liamlingdev@gmail.com
# File name: woker_base.py
# Description:
"""
"""

import asyncio
from abc import ABC, abstractmethod


class WorkerBase(ABC, asyncio.Task):
    @classmethod
    @abstractmethod
    def generate(cls):
        """
        This function generates the worker instance upon calling
        """
        ...

    @staticmethod
    @abstractmethod
    def _default_procedure():
        """
        This function should be pass as target if no exteranal callable is passed as target when the classmethod generate() is called
        """
        ...

    @staticmethod
    @abstractmethod
    def step_1():
        """
        This function should be called in _default_procedure as step 1
        """
        ...
