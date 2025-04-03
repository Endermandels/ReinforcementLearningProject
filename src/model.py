from __future__ import annotations
from toolbox import warn, error
from time import sleep
from state import *
from agent import *
from controller import Controller, TerminalController
from view import View, TerminalView
from rl_agent import RLAgent
import argparse
from random import uniform

def rotate_right(action: Action) -> Action:
    warn("* rotating right")
    if action == Action.RIGHT:
        return Action.DOWN
    if action == Action.LEFT:
        return Action.UP
    if action == Action.UP:
        return Action.RIGHT
    if action == Action.DOWN:
        return Action.LEFT

def rotate_left(action: Action) -> Action:
    warn("* rotating left")
    if action == Action.RIGHT:
        return Action.UP
    if action == Action.LEFT:
        return Action.DOWN
    if action == Action.UP:
        return Action.LEFT
    if action == Action.DOWN:
        return Action.RIGHT

def noisy_action(action: Action) -> Action:
    """ Returns possibly altered action """
    rnd = uniform(0, 1)
    if rnd < 0.8:
        return action
    if rnd < 0.9:
        return rotate_left(action)
    return rotate_right(action)

def sensed_observations(state: State) -> Observations:
    """ Returns possibly altered observations based on the state """
    return Observations(state)

class Model:
    """ Keeps track of the current game state and runs the main loop """
    def __init__(self, 
                 default_state: State, 
                 agent: Agent,
                 view: View, 
                 controller: Controller):
        self.default_state = default_state
        self.cur_state = default_state
        self.agent = agent
        self.view = view
        self.controller = controller

        self.stats = Stats()

    def _step_agent(self):
        """ Allow agent to make an action """
        # Perform action
        action = noisy_action(self.agent.update(sensed_observations(self.cur_state)))
        
        # Handle state transition
        prev_state = self.cur_state
        self.cur_state = handle_action(self.cur_state, action)
        self.stats.num_iterations += 1
        if prev_state != self.cur_state:
            self.stats.num_actions += 1
        
        # Handle terminal state
        if self.cur_state.is_terminal:
            self.agent.update(sensed_observations(self.cur_state))
            self.controller.reduce_ngames()

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

    def _update(self):
        self.view.update(self.cur_state, 
                         self.stats, 
                         self.controller)
        if not self.controller.should_simulate_game():
            self.controller.update()
            self._handle_inputs()
            if self.controller.should_simulate_game():
                self._reset_game()
        else:
            if self.cur_state.is_terminal:
                self._reset_game()
                
            if self.controller.training:
                self.agent.set_exploration_rate(0.3)
            else:
                self.agent.set_exploration_rate(0)

            self._step_agent()
            if not self.controller.training:
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
    MOVE_REWARD,
    False
)

def init_q(state: State) -> dict[tuple[int, int], float]:
    q = {}
    for y in range(len(state.grid)):
        for x in range(len(state.grid[0])):
            for action in Action:
                q[((x, y), action)] = get_tile_reward(state, (x, y))
    return q

def init_freq(state: State) -> dict[tuple[int, int], int]:
    freq = {}
    for y in range(len(state.grid)):
        for x in range(len(state.grid[0])):
            for action in Action:
                freq[((x, y), action)] = 0
    return freq

def init_view_and_controller(pygame_flag: bool) -> tuple[View, Controller]:
    if pygame_flag:
        try:
            import pygame_interface as pygi
            pygi.init_pygame()
            return pygi.PygameView(), pygi.PygameController()
        except Exception as ex:
            error(f"!!! Failed to load the pygame interface! -- {ex}")
            warn("* Defaulting to terminal view")
    return TerminalView(), TerminalController()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pygame", action="store_true")
    args = parser.parse_args()
    agent = RLAgent(init_q(TEST_STATE), init_freq(TEST_STATE))
    view, controller = init_view_and_controller(args.pygame)
    model = Model(TEST_STATE, agent, view, controller)
    model.run()

if __name__ == "__main__":
    main()