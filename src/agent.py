import agent_controller as ctrl

class Agent:
    """ AI model that takes in observations and computes the optimal acion """
    def __init__(self, controller: ctrl.AgentController):
        self.controller = controller

    def observe(self, observations):
        """ Receive observations from agent sensors """
        self._compute_action()

    def _compute_action(self):
        """ Compute optimal action """
        self._act()

    def _act(self):
        """ Send action to agent controller """
        self.controller.receive_action("test action")