from __future__ import annotations
from toolbox import warn
from state import *
import controller as ctrl
import view as vw
import agent_controller as ag_ctrl
import agent as ag
import agent_sensors as ag_ss
import argparse


class Model:
    """ Keeps track of the current game state and runs the main loop """
    def __init__(self, agent: ag.Agent, agent_controller: ag_ctrl.AgentController, 
                 agent_sensors: ag_ss.AgentSensors, default_state: State,
                 view: vw.View, controller: ctrl.Controller):
        self.view = view
        self.controller = controller
        self.default_state = default_state
        self.cur_state = default_state
        self.agent = agent
        self.agent_controller = agent_controller
        self.agent_sensors = agent_sensors
        
        self.simulating_game: bool = False # Whether the agent simulation is in progress
        self.num_iterations: int  = 0 # Number of iterations (includes illegal actions)
        self.num_actions: int = 0 # Number of successful actions
        self.final_reward: int = 0

    def _print_stats(self):
        print(f"- iterations: {self.num_iterations}")
        print(f"- actions: {self.num_actions}")
        print(f"- actions / iterations: {self.num_actions / self.num_iterations}")
        print(f"- final reward: {self.final_reward}")
        print("\n---------\n")

    def _step_agent(self):
        """ Allow agent to make an action """
        self.agent_sensors.send_observations(self.cur_state)
        prev_state = self.cur_state
        self.cur_state = handle_action(self.cur_state, self.agent_controller.get_action())
        if prev_state != self.cur_state:
            self.num_actions += 1
        self.num_iterations += 1
        if is_terminal_state(self.cur_state):
            self._print_stats()
            self.simulating_game = False

    def _handle_inputs(self):
        if self.controller.should_step():
            if is_terminal_state(self.cur_state):
                warn("* Current state is terminal; please reset game")
                return
            self._step_agent()
        elif self.controller.should_reset_game():
            self.cur_state = self.default_state
        elif self.controller.should_simulate_game():
            if is_terminal_state(self.cur_state):
                warn("* Current state is terminal; please reset game")
                return
            self.simulating_game = True

    def _update(self):
        self.view.update(self.cur_state)
        if not self.simulating_game:
            self.controller.update()
            self._handle_inputs()
        else:
            self._step_agent()

    def run(self):
        """ Run the game loop """
        while not self.controller.should_quit():
            self._update()


TEST_GRID = [
    [
        Tile(), 
        Tile(), 
        Tile(), 
        Tile(reward=1, occupying=TileSpace.ENERGY, is_terminal=True)
    ],
    [
        Tile(), 
        Tile(occupying=TileSpace.OBSTACLE), 
        Tile(), 
        Tile(reward=-1, occupying=TileSpace.TROLL, is_terminal=True)
    ],
    [
        Tile(occupying=TileSpace.ROBOT), 
        Tile(), 
        Tile(), 
        Tile()
    ]
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pygame", action="store_true")
    args = parser.parse_args()
    
    agent_controller = ag_ctrl.AgentController()
    agent = ag.RandomAgent(agent_controller)
    agent_sensors = ag_ss.AgentSensors(agent)
    view = vw.View(args.pygame)
    controller = ctrl.Controller(args.pygame)
    model = Model(agent, agent_controller, agent_sensors, State(TEST_GRID),
                  view, controller)
    model.run()

if __name__ == "__main__":
    main()