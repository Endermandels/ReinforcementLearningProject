from __future__ import annotations
import model as mdl
from random import choice

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from agent_controller import AgentController

class Agent:
    """ AI model that takes in observations and computes the optimal acion """
    def __init__(self, controller: AgentController):
        self.controller = controller
        
    def observe(self, observations):
        """ Receive observations from agent sensors """
        self._compute_action()

    def _compute_action(self):
        """ Compute optimal action """
        self._act(mdl.Action.UP)

    def _act(self, action: mdl.Action):
        """ Send action to agent controller """
        self.controller.receive_action(action)

class RandomAgent(Agent):
    def __init__(self, controller: AgentController):
        super().__init__(controller)
        
    def _compute_action(self):
        """ Compute optimal action """
        action: mdl.Action = choice([mdl.Action.UP,
                         mdl.Action.DOWN,
                         mdl.Action.LEFT,
                         mdl.Action.RIGHT,])
        self._act(action)
