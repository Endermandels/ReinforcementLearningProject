from __future__ import annotations
import agent as ag
from state import State

class AgentSensors:
    def __init__(self, agent: ag.Agent):
        self.agent = agent

    def send_observations(self, state: State):
        """ Create and send observations to Agent via a dictionary """
        self.agent.observe({'state': state})