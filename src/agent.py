from __future__ import annotations
import model as mdl
from state import State
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
        self._compute_action(observations)

    def _compute_action(self, observations: dict):
        """ Compute optimal action """
        self._act(mdl.Action.UP)

    def _act(self, action: mdl.Action):
        """ Send action to agent controller """
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
        action: mdl.Action = choice([mdl.Action.UP,
                         mdl.Action.DOWN,
                         mdl.Action.LEFT,
                         mdl.Action.RIGHT,])
        self._act(action)
