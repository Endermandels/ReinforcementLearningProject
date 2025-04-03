from __future__ import annotations
from state import *
from random import choice
from typing import NamedTuple

class Observations(NamedTuple):
    state: State

class Agent:
    """ AI model that takes in observations and computes the optimal acion """
    def __init__(self):
        self.reward = 0 # Accumulated reward over a game
        self.explore_rate: float = 0.3 # Explore 30% of the time

    def set_exploration_rate(self, rate: float):
        self.explore_rate = rate
        
    def update(self, observations: Observations) -> Action:
        """ Compute and return optimal action based on observations """
        return Action.UP

    def new_game(self):
        """ Reset agent to account for a new game """
        self.reward = 0

class RandomAgent(Agent):
    def __init__(self):
        super().__init__()

    def update(self, observations: Observations) -> Action:
        action: Action = choice([Action.UP,
                         Action.DOWN,
                         Action.LEFT,
                         Action.RIGHT,])
        return action
