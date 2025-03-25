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
        self.TITLE = "Reinforcement Learning Project"
        pygame.display.set_caption(self.TITLE)
        self.clock = pygame.time.Clock()
        
        self.GRID_CELL_SIZE = 40
        FONT_NAME = "comicsans"
        self.font_small = pygame.font.SysFont(FONT_NAME, 24)
        self.font_large = pygame.font.SysFont(FONT_NAME, 36)
    
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
    
    def draw_instructions(self, instructions: str):
        """ Draws the program instructions """
        if not self.pygame_view:
            return
        lines = instructions.split('\n')
        y_offset = 80
        for line in lines:
            text = self.font_small.render(line, True, (255, 255, 255))
            self.screen.blit(text, (50, y_offset))
            y_offset += 30
    
    def _draw_tile(self, tile: Tile, rect: pygame.Rect):
        if tile.occupying == TileSpace.OPEN:
            pygame.draw.rect(self.screen, (25, 0, 50), rect)
        elif tile.occupying == TileSpace.OBSTACLE:
            pygame.draw.rect(self.screen, (200, 200, 0), rect)
        elif tile.occupying == TileSpace.ENERGY:
            pygame.draw.rect(self.screen, (0, 200, 0), rect)
        elif tile.occupying == TileSpace.TROLL:
            pygame.draw.rect(self.screen, (200, 0, 0), rect)
        elif tile.occupying == TileSpace.ROBOT:
            pygame.draw.rect(self.screen, (0, 200, 200), rect)
    
    def _draw_grid(self, grid: list[list[Tile]]):
        """ Dynamically draw grid """
        x_offset = self.WIDTH / 2 - (self.GRID_CELL_SIZE*len(grid[0])) / 2
        y_offset = self.HEIGHT / 2 - (self.GRID_CELL_SIZE*len(grid)) / 2
        
        for y, row in enumerate(grid):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x_offset + x * self.GRID_CELL_SIZE,
                                   y_offset + y * self.GRID_CELL_SIZE,
                                   self.GRID_CELL_SIZE, self.GRID_CELL_SIZE)
                self._draw_tile(tile, rect)
                pygame.draw.rect(self.screen, (100, 75, 0), rect, 1)  # border
    
    def _draw_title(self):
        text = self.font_large.render(self.TITLE, True, (255, 255, 255))
        text_rect = text.get_rect(midtop=(self.WIDTH/2, 30))
        self.screen.blit(text, text_rect)
    
    def _draw(self, state: State):
        self._draw_title()
        self._draw_grid(state.grid)
    
    def _pygame_update(self, cur_state: State):
        self._draw(cur_state)
        pygame.display.flip()
        self.clock.tick(60)
        self.screen.fill((0, 0, 0))
    
    def update(self, cur_state: State):
        if self.pygame_view:
            self._pygame_update(cur_state)
        else:
            self._terminal_update(cur_state)