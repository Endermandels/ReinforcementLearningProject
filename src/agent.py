from __future__ import annotations
from state import Action
from random import choice

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from agent_controller import AgentController

class Agent:
    """ AI model that takes in observations and computes the optimal acion """
    def __init__(self, controller: AgentController):
        self.controller = controller
        self.reward = 0 # Accumulated reward over a game

    def observe(self, observations: dict):
        """ Receive observations from agent sensors """
        # TODO: Make a sensed function wrapper
        self._compute_action(observations)

    def _compute_action(self, observations: dict):
        """ Compute optimal action """
        # TODO: Change to tick function
        self._act(Action.UP)

    def _act(self, action: Action):
        """ Send action to agent controller """
        # TODO: Make a noisy function wrapper
        self.controller.receive_action(action)
    
    def receive_reward(self, reward):
        """ Get reward based on the previous action """
        self.reward += reward
    
    def new_game(self):
        """ Reset agent to account for a new game """
        self.reward = 0

class RandomAgent(Agent):
    def __init__(self, controller: AgentController):
        super().__init__(controller)

    def _compute_action(self, observations: dict):
        """ Compute optimal action """
        action: Action = choice([Action.UP,
                         Action.DOWN,
                         Action.LEFT,
                         Action.RIGHT,])
        self._act(action)
