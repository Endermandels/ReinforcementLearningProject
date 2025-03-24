from toolbox import BColors
from state import *

class View:
    def __init__(self, pygame_view: bool = False):
        self.pygame_view = pygame_view # Whether to display pygame graphics or print to terminal
    
    def _print_grid(self, grid: list[list[Tile]]):
        string = ""
        for row in grid:
            for tile in row:
                if tile.is_terminal:
                    string += BColors.BOLD
                    
                if tile.occupying == TileSpace.OBSTACLE:
                    string += BColors.YELLOW
                elif tile.occupying == TileSpace.ROBOT:
                    string += BColors.CYAN
                elif tile.reward > 0:
                    string += BColors.GREEN
                elif tile.reward < 0:
                    string += BColors.RED
                    
                string += f" {tile.occupying.value} "
                string += BColors.ENDC
            string += "\n"
        print(string)
        
    def _print_state(self, state: State):
        self._print_grid(state.grid)
    
    def _terminal_update(self, cur_state: State):
        self._print_state(cur_state)
        
    def _pygame_update(self, cur_state: State):
        pass
    
    def update(self, cur_state: State):
        if self.pygame_view:
            self._pygame_update(cur_state)
        else:
            self._terminal_update(cur_state)