from toolbox import warn

PYGAME = False

try:
    import pygame
    PYGAME = True
except ImportError as e:
    warn(f"* {e}")


class Controller:
    """ Handles user inputs (either gui or terminal) """
    def __init__(self, pygame_view: bool = False):
        self.pygame_view = pygame_view # Whether to use pygame for display or the terminal
        if not PYGAME:
            warn("* Setting pygame_view to false because Pygame is not imported")
            self.pygame_view = False
        self.quit_input = False # Whether to quit the program
        self.step_input = False # Whether to step through the next agent action
        self.reset_game = False # Whether to reset the game state
        self.simulate_game = False # Whether to simulate a game from current state to terminal state

    def _handle_pygame_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_input = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.quit_input = True
        
    def _update_pygame(self):
        self._handle_pygame_input()
    
    def _handle_terminal_input(self):
        # Parse user input
        user_input = input("What would you like to do?\n"
            "  1) quit\n"
            "  2) reset game\n"
            "  3) step through next agent action\n"
            "  4) simulate agent playing\n"
            ">> "
        )
        if not user_input.isdigit():
            warn("* Please input a valid number")
            return
        user_input = int(user_input)
        
        # Determine action based on user input
        if user_input == 1:
            self.quit_input = True
        elif user_input == 2:
            self.reset_game = True
        elif user_input == 3:
            self.step_input = True
        elif user_input == 4:
            self.simulate_game = True
        else:
            warn(f"* Unknown option {user_input}; input a valid number")
    
    def _update_terminal(self):
        self._handle_terminal_input()
    
    def update(self):
        if self.pygame_view:
            self._update_pygame()
        else:
            self._update_terminal()
    
    def should_quit(self) -> bool:
        temp = self.quit_input
        self.quit_input = False
        return temp
    
    def should_reset_game(self) -> bool:
        temp = self.reset_game
        self.reset_game = False
        return temp

    def should_step(self) -> bool:
        temp = self.step_input
        self.step_input = False
        return temp
        
    def should_simulate_game(self) -> bool:
        temp = self.simulate_game
        self.simulate_game = False
        return temp