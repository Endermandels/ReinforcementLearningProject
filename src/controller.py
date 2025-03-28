from toolbox import warn
from pygame_handler import *

class Controller:
    """ Handles user inputs """
    def __init__(self):
        self.quit_input = False # Whether to quit the program
        self.step_input = False # Whether to step through the next agent action
        self.reset_game = False # Whether to reset the game state
        self.simulate_game = False # Whether to simulate a game from current state to terminal state
        self.INSTRUCTIONS = ""

    def _handle_inputs(self):
        """ Set appropriate flags based on inputs """
        pass

    def update(self):
        self._handle_inputs()
    
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

class TerminalController(Controller):
    def __init__(self):
        super().__init__()
        self.INSTRUCTIONS = "What would you like to do?\n" \
            "  1) quit\n" \
            "  2) reset game\n" \
            "  3) step through next agent action\n" \
            "  4) simulate agent playing\n"
    
    def _handle_inputs(self):
        # Parse user input
        user_input = input()
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

class PygameController(Controller):
    def __init__(self, pygame_handler: PygameHandler):
        super().__init__()
        assert PYGAME and pygame_handler, "Pygame must be installed" \
            " and PygameHandler must be initialized; or use TerminalController"
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
            