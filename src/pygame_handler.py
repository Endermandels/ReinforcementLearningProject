from toolbox import *
from enum import Enum

PYGAME = False # Whether pygame module is imported

try:
    import pygame
    PYGAME = True
except ImportError as e:
    warn(f"* {e}")

class PygameEvent(Enum):
    QUIT = 0
    K_ESCAPE = 1
    K_RETURN = 2
    K_PERIOD = 3
    K_1 = 4
    K_2 = 5
    K_3 = 6
    K_4 = 7
    K_5 = 8
    K_6 = 9
    K_7 = 10
    K_8 = 11
    K_9 = 12
    K_0 = 13
    

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
                if event.key == pygame.K_RETURN:
                    events.append(PygameEvent.K_RETURN)
                if event.key == pygame.K_PERIOD:
                    events.append(PygameEvent.K_PERIOD)
                if event.key == pygame.K_1:
                    events.append(PygameEvent.K_1)
                if event.key == pygame.K_2:
                    events.append(PygameEvent.K_2)
                if event.key == pygame.K_3:
                    events.append(PygameEvent.K_3)
                if event.key == pygame.K_4:
                    events.append(PygameEvent.K_4)
                if event.key == pygame.K_5:
                    events.append(PygameEvent.K_5)
                if event.key == pygame.K_6:
                    events.append(PygameEvent.K_6)
                if event.key == pygame.K_7:
                    events.append(PygameEvent.K_7)
                if event.key == pygame.K_8:
                    events.append(PygameEvent.K_8)
                if event.key == pygame.K_9:
                    events.append(PygameEvent.K_9)
                if event.key == pygame.K_0:
                    events.append(PygameEvent.K_0)
        return events