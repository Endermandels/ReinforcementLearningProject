from config import *
from toolbox import *
from state import *

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

    def _display_instructions(self, instructions: str):
        """ Display instructions given by the Controller """
        pass

    def update(self, cur_state: State, stats: Stats, instructions: str, simulating_game: bool):
        self.simulating_game = simulating_game
        self._display_header()
        self._display_state(cur_state)
        self._display_stats(stats)
        self._display_instructions(instructions)

class TerminalView(View):
    def __init__(self):
        super().__init__()

    def _print_grid(self, grid: list[list[Tile]]):
        string = ""
        for row in grid:
            for tile in row:
                if tile.is_terminal:
                    string += BColors.BOLD

                if tile.occupying == TileSpace.OBSTACLE:
                    string += OBSTACLE_COL
                elif tile.occupying == TileSpace.ROBOT:
                    string += ROBOT_COL
                elif tile.reward > 0:
                    string += REWARD_COL
                elif tile.reward < 0:
                    string += PAIN_COL
                elif tile.occupying == TileSpace.OPEN:
                    string += OPEN_COL

                string += f" {tile.occupying.value} "
                string += BColors.ENDC
            string += "\n"
        print(string)

    def _display_state(self, state: State):
        self._print_grid(state.grid)

    def _display_stats(self, stats: Stats):
        if self.simulating_game:
            return
        print(f"- iterations: {stats.num_iterations}")
        print(f"- actions: {stats.num_actions}")
        act_per_iter = stats.num_actions / stats.num_iterations if stats.num_iterations > 0 else 0
        print(f"- actions / iterations: {round(act_per_iter, 3)}")
        print(f"- final reward: {stats.final_reward}")
        print()

    def _display_instructions(self, instructions: str):
        if self.simulating_game:
            return
        print(instructions)
        print(">> ", end="")

