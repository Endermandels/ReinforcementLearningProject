from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model import Action

class AgentController:
    def __init__(self):
        self.action: Action = None

    def receive_action(self, action: Action):
        """ Recieves, modifies and stores given action from Agent """
        self.action = action

    def get_action(self) -> Action:
        """ Returns the stored action, setting action to None """
        temp = self.action
        self.action = None
        return temp