from __future__ import annotations
from toolbox import warn, error
from time import sleep
from state import *
import controller as ctrl
import view as vw
import agent_controller as ag_ctrl
import agent as ag
import rl_agent as rl_ag
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
        self.stats = Stats()

    def _step_agent(self):
        """ Allow agent to make an action """
        self.agent_sensors.send_observations(self.cur_state)
        
        prev_state = self.cur_state
        self.cur_state = handle_action(self.cur_state, self.agent_controller.get_action())
        if prev_state != self.cur_state:
            self.stats.num_actions += 1
        
        self.stats.num_iterations += 1
        if self.cur_state.is_terminal:
            self.agent_sensors.send_observations(self.cur_state)
            self.simulating_game = False
        
        self.stats.reward = self.agent.reward

    def _reset_game(self):
        self.cur_state = self.default_state
        self.stats = Stats()
        self.agent.new_game()

    def _handle_inputs(self):
        if self.controller.should_step():
            if self.cur_state.is_terminal:
                warn("* Current state is terminal; please reset game")
                return
            self._step_agent()
        elif self.controller.should_reset_game():
            self._reset_game()
        elif self.controller.should_simulate_game():
            if self.cur_state.is_terminal:
                warn("* Current state is terminal; please reset game")
                return
            self.simulating_game = True

    def _update(self):
        self.view.update(self.cur_state, 
                         self.stats, 
                         self.controller,
                         self.simulating_game)
        if not self.simulating_game:
            self.controller.update()
            self._handle_inputs()
        else:
            self._step_agent()
            sleep(self.controller.simulation_wait_time)

    def run(self):
        """ Run the game loop """
        while not self.controller.should_quit():
            self._update()

TEST_GRID = (
    (
        Tile.OPEN,
        Tile.OPEN,
        Tile.OPEN,
        Tile.OPEN
    ),
    (
        Tile.OPEN,
        Tile.OBSTACLE,
        Tile.OPEN,
        Tile.OPEN
    ),
    (
        Tile.OPEN,
        Tile.OPEN,
        Tile.OPEN,
        Tile.OPEN
    ),
)
TEST_STATE = State(
    TEST_GRID, 
    (0, 2),
    (3, 1),
    (3, 0),
    0,
    False
)

def init_view_and_controller(pygame_flag: bool) -> tuple[vw.View, ctrl.Controller]:
    if pygame_flag:
        try:
            import pygame_interface as pygi
            pygi.init_pygame()
            return pygi.PygameView(), pygi.PygameController()
        except Exception as ex:
            error(f"!!! Failed to load the pygame interface! -- {ex}")
            warn("* Defaulting to terminal view")
    return vw.TerminalView(), ctrl.TerminalController()
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pygame", action="store_true")
    args = parser.parse_args()

    agent_controller = ag_ctrl.AgentController()
    agent = ag.RandomAgent(agent_controller)
    agent_sensors = ag_ss.AgentSensors(agent)

    view, controller = init_view_and_controller(args.pygame)

    model = Model(agent, agent_controller, agent_sensors, TEST_STATE, view, controller)
    model.run()

if __name__ == "__main__":
    main()