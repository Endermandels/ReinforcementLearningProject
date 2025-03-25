from toolbox import BColors, warn
from state import *

PYGAME = False

try:
    import pygame
    PYGAME = True
except ImportError as e:
    warn(f"* {e}")

class View:
    def __init__(self, pygame_view: bool = False):
        self.pygame_view = pygame_view # Whether to display pygame graphics or print to terminal
        if not PYGAME:
            warn("* Setting pygame_view to false because Pygame is not imported")
            self.pygame_view = False
        if self.pygame_view:
            self._pygame_init()
    
    def _pygame_init(self):
        pygame.init()
        self.WIDTH = 1080
        self.HEIGHT = 720
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
    
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
        pygame.display.flip()
        self.clock.tick(60)
        self.screen.fill((0, 0, 0))
        pygame.display.set_caption("Reinforcement Learning Project")
    
    def update(self, cur_state: State):
        if self.pygame_view:
            self._pygame_update(cur_state)
        else:
            self._terminal_update(cur_state)