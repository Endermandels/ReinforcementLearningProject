from toolbox import BColors
import model as mdl

class View:
    def __init__(self, pygame_view: bool = False):
        self.pygame_view = pygame_view # Whether to display pygame graphics or print to terminal
    
    def _print_grid(self, grid: list[list[mdl.Tile]]):
        string = ""
        for row in grid:
            for tile in row:
                if tile.is_terminal:
                    string += BColors.BOLD
                    
                if tile.is_obstacle():
                    string += BColors.YELLOW
                elif tile.has_robot():
                    string += BColors.CYAN
                elif tile.reward > 0:
                    string += BColors.GREEN
                elif tile.reward < 0:
                    string += BColors.RED
                    
                string += f" {tile.occupying} "
                string += BColors.ENDC
            string += "\n"
        print(string)
        
    def _print_state(self, state: mdl.State):
        self._print_grid(state.grid)
    
    def _terminal_update(self, cur_state: mdl.State):
        self._print_state(cur_state)
        
    def _pygame_update(self, cur_state: mdl.State):
        pass
    
    def update(self, cur_state: mdl.State):
        if self.pygame_view:
            self._pygame_update(cur_state)
        else:
            self._terminal_update(cur_state)