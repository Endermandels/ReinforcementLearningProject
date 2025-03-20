from toolbox import warn

class Controller:
    """ Handles user inputs (either gui or terminal) """
    def __init__(self, pygame_view: bool = False):
        self.pygame_view = pygame_view # Whether to use pygame for display or the terminal
        self.quit_input = False # Whether to quit the program

    def _update_pygame(self):
        pass
    
    def _handle_terminal_input(self):
        # Parse user input
        user_input = input("What would you like to do?\n"
            "  1) quit\n"
            ">> "
        )
        if not user_input.isdigit():
            warn("* Please input a valid number")
            return
        user_input = int(user_input)
        
        # Determine action based on user input
        if user_input == 1:
            self.quit_input = True
        else:
            warn(f"* Unknown option {user_input}; input a valid number")
    
    def _update_terminal(self):
        self._handle_terminal_input()
    
    def update(self):
        if self.pygame_view:
            self._update_pygame()
        else:
            self._update_terminal()
    
    def should_quit(self):
        """ Returns whether the program should exit """
        return self.quit_input
