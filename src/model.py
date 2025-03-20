import controller as ctrl
import view as vw

class Tile:
    def __init__(self, reward: int = 0, is_obstacle: bool = False, is_terminal: bool = False,
                 has_robot: bool = False):
        self.reward = reward
        self.is_obstacle = is_obstacle
        self.is_terminal = is_terminal
        self.has_robot = has_robot

class State:
    def __init__(self, initial_grid: list[list[Tile]]=None):
        self.grid: list[list[Tile]] = initial_grid
        if not self.grid:
            self.grid = self._init_grid()
    
    def _init_grid(self) -> list[list[Tile]]:
        grid = [
            [
                Tile(), Tile(), Tile(), Tile(reward=1, is_terminal=True)
            ],
            [
                Tile(), Tile(is_obstacle=True), Tile(), Tile(reward=-1, is_terminal=True)
            ],
            [
                Tile(has_robot=True), Tile(), Tile(), Tile()
            ]
        ]
        return grid
        

class Model:
    """ Keeps track of the current game state and runs the main loop """
    def __init__(self):
        self.controller = ctrl.Controller()
        self.view = vw.View()
        self.cur_state = State()

    def _update(self):
        self.view.update(self.cur_state)
        self.controller.update()

    def run(self):
        """ Run the game loop """
        while not self.controller.should_quit():
            self._update()

def main():
    model = Model()
    model.run()

if __name__ == "__main__":
    main()