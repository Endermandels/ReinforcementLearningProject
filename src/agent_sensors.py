import agent as ag

class AgentSensors:
    def __init__(self, agent: ag.Agent):
        self.agent = agent

    def send_observations(self, state):
        """ Create and send observations to Agent """
        self.agent.observe(None)