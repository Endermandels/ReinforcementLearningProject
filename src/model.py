from time import sleep
from controller import Controller

class Model:
    """ Keeps track of the current game state and runs the main loop """
    def __init__(self):
        self.controller = Controller()

    def update(self):
        self.controller.update()

    def run(self):
        """ Run the game loop """
        while not self.controller.should_quit():
            self.update()

def main():
    model = Model()
    model.run()

if __name__ == "__main__":
    main()