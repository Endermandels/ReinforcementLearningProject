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
        self.simulation_wait_time = 0 # How long to wait inbetween steps while simulating the agent game

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
                "  4) simulate agent playing\n" \
                "  5) set simulation speed (steps/sec)\n"
    
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
        elif user_input == 5:
            user_input = input("Rate: ")
            while True:
                try:
                    rate = float(user_input)
                    break
                except:
                    warn("* Please input a valid float")
                    user_input = input("Rate: ")
            self.simulation_wait_time = 1 / rate if rate > 0 else 0
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
                "  4) simulate agent playing\n" \
                "  5) set simulation speed (steps/sec)\n"
        self.simulation_rate_input = ""
        
    def _handle_inputs(self):
        for event in self.pygame_handler.get_events():
            if event == PygameEvent.QUIT:
                self.quit_input = True
            if event == PygameEvent.K_ESCAPE:
                self.quit_input = True
            if not self.simulation_rate_input:
                if event == PygameEvent.K_1:
                    self.quit_input = True
                if event == PygameEvent.K_2:
                    self.reset_game = True
                if event == PygameEvent.K_3:
                    self.step_input = True
                if event == PygameEvent.K_4:
                    self.simulate_game = True
                if event == PygameEvent.K_5:
                    self.simulation_rate_input = "0"
            else:
                if event == PygameEvent.K_RETURN:
                    try:
                        rate = float(self.simulation_rate_input)
                        self.simulation_wait_time = 1 / rate if rate > 0 else 0
                        self.simulation_rate_input = ""
                    except:
                        warn("* Please input a valid float")
                        self.simulation_rate_input = "0"
                if event == PygameEvent.K_1:
                    self.simulation_rate_input += "1"
                if event == PygameEvent.K_2:
                    self.simulation_rate_input += "2"
                if event == PygameEvent.K_3:
                    self.simulation_rate_input += "3"
                if event == PygameEvent.K_4:
                    self.simulation_rate_input += "4"
                if event == PygameEvent.K_5:
                    self.simulation_rate_input += "5"
                if event == PygameEvent.K_6:
                    self.simulation_rate_input += "6"
                if event == PygameEvent.K_7:
                    self.simulation_rate_input += "7"
                if event == PygameEvent.K_8:
                    self.simulation_rate_input += "8"
                if event == PygameEvent.K_9:
                    self.simulation_rate_input += "9"
                if event == PygameEvent.K_0:
                    self.simulation_rate_input += "0"
                if event == PygameEvent.K_PERIOD:
                    self.simulation_rate_input += "."
                    
            