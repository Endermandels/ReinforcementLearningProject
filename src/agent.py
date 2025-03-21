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
        
        # TODO: Make this smarter
        self.move_up = 2
        self.move_right = 3

    def observe(self, observations):
        """ Receive observations from agent sensors """
        self._compute_action()

    def _compute_action(self):
        """ Compute optimal action """
        # TODO: Make this smarter
        action = choice([mdl.Action.UP,
                         mdl.Action.DOWN,
                         mdl.Action.LEFT,
                         mdl.Action.RIGHT,])
        if self.move_up:
            self.move_up -= 1
            action = mdl.Action.UP
        elif self.move_right:
            self.move_right -= 1
            action = mdl.Action.RIGHT
        self._act(action)

    def _act(self, action: mdl.Action):
        """ Send action to agent controller """
        self.controller.receive_action(action)