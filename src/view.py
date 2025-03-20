from toolbox import cprint, bcolors
import model as mdl

class View:
    def __init__(self, pygame_view: bool = False):
        self.pygame_view = pygame_view # Whether to display pygame graphics or print to terminal
    
    def _print_grid(self, grid: list[list[mdl.Tile]]):
        string = ""
        for row in grid:
            for tile in row:
                if tile.is_terminal:
                    string += bcolors.BOLD
                    
                if tile.is_obstacle:
                    string += bcolors.YELLOW
                    string += " # "  # Obstacle
                elif tile.has_robot:
                    string += bcolors.CYAN
                    string += " @ "
                elif tile.reward:
                    if tile.reward > 0:
                        string += bcolors.GREEN
                    else:
                        string += bcolors.RED
                    string += f" {tile.reward:+} "  # Show terminal rewards (+1, -1)
                else:
                    string += " . "  # Normal tile
                string += bcolors.ENDC
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