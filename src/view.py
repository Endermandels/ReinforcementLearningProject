from config import *
from toolbox import *
from state import *
from pygame_handler import *

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

class PygameView(View):
    def __init__(self, pygame_handler: PygameHandler):
        super().__init__()
        self.pygame_handler = pygame_handler
        
        self.WIDTH = 1080
        self.HEIGHT = 720
        self.screen = self.pygame_handler.create_screen(self.WIDTH, self.HEIGHT)
        self.TITLE = "Reinforcement Learning Project"
        self.pygame_handler.set_caption(self.TITLE)
        self.clock = self.pygame_handler.get_clock()
        
        self.text_y_offset = 0
        self.LINE_SPACING = 30
        self.LEFT_LINE_ALIGN = 50
        self.GRID_CELL_SIZE = 40
        
        FONT_NAME = "comicsans"
        self.font_small = self.pygame_handler.create_font(FONT_NAME, 24)
        self.font_large = self.pygame_handler.create_font(FONT_NAME, 36)
        
        self.title_img = self.font_large.render(self.TITLE, True, (255, 255, 255))
        self.title_rect = self.title_img.get_rect(midtop=(self.WIDTH/2, 30))
    
    def _draw_tile(self, tile: Tile, rect):
        if tile.occupying == TileSpace.OPEN:
            self.pygame_handler.draw_rect(self.screen, (25, 0, 50), rect)
        elif tile.occupying == TileSpace.OBSTACLE:
            self.pygame_handler.draw_rect(self.screen, (200, 200, 0), rect)
        elif tile.occupying == TileSpace.ENERGY:
            self.pygame_handler.draw_rect(self.screen, (0, 200, 0), rect)
        elif tile.occupying == TileSpace.TROLL:
            self.pygame_handler.draw_rect(self.screen, (200, 0, 0), rect)
        elif tile.occupying == TileSpace.ROBOT:
            self.pygame_handler.draw_rect(self.screen, (0, 200, 200), rect)    
    
    def _draw_grid(self, grid: list[list[Tile]]):
        x_offset = self.WIDTH / 2 - (self.GRID_CELL_SIZE*len(grid[0])) / 2
        y_offset = self.HEIGHT / 2 - (self.GRID_CELL_SIZE*len(grid)) / 2
        
        for y, row in enumerate(grid):
            for x, tile in enumerate(row):
                rect = self.pygame_handler.create_rect(x_offset + x * self.GRID_CELL_SIZE,
                                                       y_offset + y * self.GRID_CELL_SIZE,
                                                       self.GRID_CELL_SIZE, 
                                                       self.GRID_CELL_SIZE)
                self._draw_tile(tile, rect)
                
                # border
                if tile.is_terminal:
                    self.pygame_handler.draw_rect(self.screen, (255, 255, 255), rect, 2)
                else:
                    self.pygame_handler.draw_rect(self.screen, (100, 75, 0), rect, 2)  
    
    def _display_header(self):
        # Update pygame stuff
        self.pygame_handler.display_flip()
        self.clock.tick(60)
        self.screen.fill((0,0,0))
        
        self.screen.blit(self.title_img, self.title_rect)
    
    def _display_state(self, state: State):
        self._draw_grid(state.grid)
    
    def _display_stats(self, stats: Stats):
        iter_text = self.font_small.render(f"iterations: {stats.num_iterations}", 
                                           True, 
                                           (255,255,255))
        act_text = self.font_small.render(f"actions: {stats.num_actions}", 
                                          True, 
                                          (255,255,255))
        act_per_iter = stats.num_actions / stats.num_iterations if stats.num_iterations > 0 else 0
        act_per_iter_text = self.font_small.render(f"actions / iterations: {round(act_per_iter, 3)}",
                                                   True, 
                                                   (255,255,255))
        final_reward_text = self.font_small.render(f"final reward: {stats.final_reward}", 
                                                   True, 
                                                   (255,255,255))
        
        self.text_y_offset = 80
        self.screen.blit(iter_text, (self.LEFT_LINE_ALIGN, self.text_y_offset))
        self.text_y_offset += self.LINE_SPACING
        self.screen.blit(act_text, (self.LEFT_LINE_ALIGN, self.text_y_offset))
        self.text_y_offset += self.LINE_SPACING
        self.screen.blit(act_per_iter_text, (self.LEFT_LINE_ALIGN, self.text_y_offset))
        self.text_y_offset += self.LINE_SPACING
        self.screen.blit(final_reward_text, (self.LEFT_LINE_ALIGN, self.text_y_offset))
        self.text_y_offset += self.LINE_SPACING*2
    
    def _display_instructions(self, instructions: str):
        lines = instructions.split('\n')
        for line in lines:
            text = self.font_small.render(line, True, (255, 255, 255))
            self.screen.blit(text, (self.LEFT_LINE_ALIGN, self.text_y_offset))
            self.text_y_offset += self.LINE_SPACING