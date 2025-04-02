from config import *
from toolbox import *
from state import *
import controller as ctrl

class View:
    """ Displays game state and user instructions """
    def __init__(self):
        self.simulating_game = False

    def _display_header(self):
        """ Display any header info on every update call """
        pass

    def _display_state(self, state: State):
        """ Display state, mainly the grid """
        pass

    def _display_stats(self, stats: Stats):
        """ Display stats of the current run """
        pass
    
    def _display_controller_prompts(self, controller: ctrl.Controller):
        """ Display instructions given by the Controller """
        pass
    
    def update(self, cur_state: State, stats: Stats, controller: ctrl.Controller, simulating_game: bool):
        self.simulating_game = simulating_game
        self._display_header()
        self._display_state(cur_state)
        self._display_stats(stats)
        self._display_controller_prompts(controller)

class TerminalView(View):
    def __init__(self):
        super().__init__()

    def _display_state(self, state: State):
        string = ""
        for y, row in enumerate(state.grid):
            for x, tile in enumerate(row):
                pos = (x, y)
                if is_terminal_tile(state, pos):
                    string += BColors.BOLD

                if pos == state.robot_pos:
                    string += f"{ROBOT_COL} {MovableObject.ROBOT} "
                elif pos == state.energy_pos:
                    string += f"{REWARD_COL} {MovableObject.ENERGY} "
                elif pos == state.troll_pos:
                    string += f"{PAIN_COL} {MovableObject.TROLL} "
                elif tile == Tile.OBSTACLE:
                    string += f"{OBSTACLE_COL} {tile.value} "
                elif tile == Tile.OPEN:
                    string += f"{OPEN_COL} {tile.value} "

                string += BColors.ENDC
            string += "\n"
        print(string)

    def _display_stats(self, stats: Stats):
        if self.simulating_game:
            return
        print(f"- iterations: {stats.num_iterations}")
        print(f"- actions: {stats.num_actions}")
        act_per_iter = stats.num_actions / stats.num_iterations if stats.num_iterations > 0 else 0
        print(f"- actions / iterations: {round(act_per_iter, 3)}")
        print(f"- reward: {stats.reward}")
        print()
    
    def _display_controller_prompts(self, controller: ctrl.TerminalController):
        if self.simulating_game:
            return
        print(controller.INSTRUCTIONS)
        print(">> ", end="")
