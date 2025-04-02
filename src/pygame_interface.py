import pygame
from toolbox import *
from controller import Controller
from view import View
from state import *

def init_pygame():
    pygame.init()

class PygameController(Controller):
    def __init__(self):
        super().__init__()
        self.INSTRUCTIONS = "What would you like to do?\n" \
                "  1) quit\n" \
                "  2) reset game\n" \
                "  3) step through next agent action\n" \
                "  4) simulate agent playing\n" \
                "  5) set simulation speed (steps/sec)\n"
        self.simulation_rate_input = ""
        
    def _handle_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_input = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_input = True
                if not self.simulation_rate_input:
                    if event.key == pygame.K_1:
                        self.quit_input = True
                    if event.key == pygame.K_2:
                        self.reset_game = True
                    if event.key == pygame.K_3:
                        self.step_input = True
                    if event.key == pygame.K_4:
                        self.simulate_game = True
                    if event.key == pygame.K_5:
                        self.simulation_rate_input = "0"
                else:
                    if event.key == pygame.K_RETURN:
                        try:
                            rate = float(self.simulation_rate_input)
                            self.simulation_wait_time = 1 / rate if rate > 0 else 0
                            self.simulation_rate_input = ""
                        except:
                            warn("* Please input a valid float")
                            self.simulation_rate_input = "0"
                    if event.key == pygame.K_1:
                        self.simulation_rate_input += "1"
                    if event.key == pygame.K_2:
                        self.simulation_rate_input += "2"
                    if event.key == pygame.K_3:
                        self.simulation_rate_input += "3"
                    if event.key == pygame.K_4:
                        self.simulation_rate_input += "4"
                    if event.key == pygame.K_5:
                        self.simulation_rate_input += "5"
                    if event.key == pygame.K_6:
                        self.simulation_rate_input += "6"
                    if event.key == pygame.K_7:
                        self.simulation_rate_input += "7"
                    if event.key == pygame.K_8:
                        self.simulation_rate_input += "8"
                    if event.key == pygame.K_9:
                        self.simulation_rate_input += "9"
                    if event.key == pygame.K_0:
                        self.simulation_rate_input += "0"
                    if event.key == pygame.K_PERIOD:
                        self.simulation_rate_input += "."
                    
            

class PygameView(View):
    def __init__(self):
        super().__init__()
        
        self.WIDTH = 1080
        self.HEIGHT = 720
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.TITLE = "Reinforcement Learning Project"
        pygame.display.set_caption(self.TITLE)
        self.clock = pygame.time.Clock()
        
        self.text_y_offset = 0
        self.LINE_SPACING = 30
        self.LEFT_LINE_ALIGN = 50
        self.GRID_CELL_SIZE = 40
        
        FONT_NAME = "comicsans"
        self.font_small = pygame.font.SysFont(FONT_NAME, 24)
        self.font_large = pygame.font.SysFont(FONT_NAME, 36)
        
        self.title_img = self.font_large.render(self.TITLE, True, (255, 255, 255))
        self.title_rect = self.title_img.get_rect(midtop=(self.WIDTH/2, 30))
    
    def _display_header(self):
        # Update pygame stuff
        pygame.display.flip()
        self.clock.tick(60)
        self.screen.fill((0,0,0))
        
        self.screen.blit(self.title_img, self.title_rect)
    
    def _display_state(self, state: State):
        x_offset = self.WIDTH / 2 - (self.GRID_CELL_SIZE*len(state.grid[0])) / 2
        y_offset = self.HEIGHT / 2 - (self.GRID_CELL_SIZE*len(state.grid)) / 2
        
        for y, row in enumerate(state.grid):
            for x, tile in enumerate(row):
                pos = (x, y)
                rect = pygame.Rect(x_offset + x * self.GRID_CELL_SIZE,
                                                       y_offset + y * self.GRID_CELL_SIZE,
                                                       self.GRID_CELL_SIZE, 
                                                       self.GRID_CELL_SIZE)
                
                if pos == state.robot_pos:
                    pygame.draw.rect(self.screen, (0, 200, 200), rect)    
                elif pos == state.troll_pos:
                    pygame.draw.rect(self.screen, (200, 0, 0), rect)
                elif pos == state.energy_pos:
                    pygame.draw.rect(self.screen, (0, 200, 0), rect)
                elif tile == Tile.OBSTACLE:
                    pygame.draw.rect(self.screen, (200, 200, 0), rect)
                elif tile == Tile.OPEN:
                    pygame.draw.rect(self.screen, (25, 0, 50), rect)
                    
                # Terminal tile border
                if is_terminal_tile(state, pos):
                    pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)
                else:
                    pygame.draw.rect(self.screen, (100, 75, 0), rect, 2)
    
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
        final_reward_text = self.font_small.render(f"reward: {stats.reward}", 
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
    
    def _display_controller_prompts(self, controller: PygameController):
        lines = controller.INSTRUCTIONS.split('\n')
        for line in lines:
            text = self.font_small.render(line, True, (255, 255, 255))
            self.screen.blit(text, (self.LEFT_LINE_ALIGN, self.text_y_offset))
            self.text_y_offset += self.LINE_SPACING
        
        if controller.simulation_rate_input:
            self.text_y_offset += self.LINE_SPACING
            text = self.font_small.render(">> "+ controller.simulation_rate_input[1:], 
                                          True,
                                          (255,255,255))
            self.screen.blit(text, (self.LEFT_LINE_ALIGN, self.text_y_offset))
