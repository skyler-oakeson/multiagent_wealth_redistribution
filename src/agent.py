"""
This Module is for declaring the Agent class and its corressponding methods and
types.
"""

from typing import Callable


type AgentStrategies = Callable[[Move], ]

class Agent:
    self.id: int

    def __init__(self, id: int):
        self.id: int = id
        self.strategies = []
