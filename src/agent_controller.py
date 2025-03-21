class AgentController:
    def __init__(self):
        self.action = None

    def receive_action(self, action):
        """ Recieves, modifies and stores given action from Agent """
        self.action = action

    def get_action(self):
        """ Returns the stored action, setting action to None """
        temp = self.action
        self.action = None
        return temp