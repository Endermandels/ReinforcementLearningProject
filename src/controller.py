from toolbox import warn

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
