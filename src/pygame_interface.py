import pygame
from toolbox import *
from enum import Enum
from controller import Controller
from view import View
from state import *

class PygameEvent(Enum):
    QUIT = 0
    K_ESCAPE = 1
    K_1 = 2
    K_2 = 3
    K_3 = 4
    K_4 = 5

class PygameHandler:
    """ Custom API for common pygame functions """
    def __init__(self):
        pygame.init()

    def create_screen(self, w: int, h: int) -> pygame.Surface:
        return pygame.display.set_mode((w, h))

    def set_caption(self, cap: str):
        pygame.display.set_caption(cap)

    def get_clock(self) -> pygame.time.Clock:
        return pygame.time.Clock()

    def create_font(self, name: str, size: int) -> pygame.font.Font:
        return pygame.font.SysFont(name, size)

    def display_flip(self):
        pygame.display.flip()

    def create_rect(self, x: float, y: float, w: float, h: float) -> pygame.Rect:
        return pygame.Rect(x, y, w, h)

    def draw_rect(self,
                  screen: pygame.Surface,
                  color: tuple[int, int, int],
                  rect: pygame.Rect,
                  border_size: int = 0):
        pygame.draw.rect(screen, color, rect, width=border_size)

    def get_events(self) -> list[PygameEvent]:
        events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events.append(PygameEvent.QUIT)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    events.append(PygameEvent.K_ESCAPE)
                if event.key == pygame.K_1:
                    events.append(PygameEvent.K_1)
                if event.key == pygame.K_2:
                    events.append(PygameEvent.K_2)
                if event.key == pygame.K_3:
                    events.append(PygameEvent.K_3)
                if event.key == pygame.K_4:
                    events.append(PygameEvent.K_4)
        return events


class PygameController(Controller):
    def __init__(self, pygame_handler: PygameHandler):
        super().__init__()
        assert pygame_handler, "PygameHandler must be initialized; or use TerminalController"
        self.pygame_handler = pygame_handler
        self.INSTRUCTIONS = "What would you like to do?\n" \
            "  1) quit\n" \
            "  2) reset game\n" \
            "  3) step through next agent action\n" \
            "  4) simulate agent playing\n"

    def _handle_inputs(self):
        for event in self.pygame_handler.get_events():
            if event == PygameEvent.QUIT:
                self.quit_input = True
            if event == PygameEvent.K_ESCAPE or event == PygameEvent.K_1:
                self.quit_input = True
            if event == PygameEvent.K_2:
                self.reset_game = True
            if event == PygameEvent.K_3:
                self.step_input = True
            if event == PygameEvent.K_4:
                self.simulate_game = True

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