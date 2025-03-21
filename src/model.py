from __future__ import annotations
from toolbox import warn
import controller as ctrl
import view as vw
import agent_controller as ag_ctrl
import agent as ag
import agent_sensors as ag_ss

class Action:
    """ Available actions """
    UP = (0,-1)
    DOWN = (0,1)
    LEFT = (-1,0)
    RIGHT = (1,0)

class Tile:
    OBSTACLE = '#'
    ROBOT = '@'
    OPEN = '.'
    ENERGY = '$'
    TROLL = '!'
    
    def __init__(self, reward: int = 0, occupying: str = '.', is_terminal: bool = False):
        self.reward = reward # Reward for agent reaching this tile
        self.occupying = occupying # What is occupying this tile
        self.is_terminal = is_terminal # End space
    
    def add_robot(self):
        self.occupying = Tile.ROBOT
    
    def remove_robot(self):
        self.occupying = Tile.OPEN
    
    def is_obstacle(self) -> bool:
        return self.occupying == Tile.OBSTACLE

    def has_robot(self) -> bool:
        return self.occupying == Tile.ROBOT
    
    def copy(self) -> Tile:
        return Tile(self.reward, self.occupying, self.is_terminal)

class State:
    def __init__(self, grid: list[list[Tile]]=None, robot_pos: tuple[int,int]=None):
        assert (grid is None) == (robot_pos is None) # Make sure that both or neither are specified
        self.grid = grid
        self.robot_pos = robot_pos
        if not self.grid:
            self.grid, self.robot_pos = self._init_grid()
    
    def _init_grid(self) -> tuple[list[list[Tile]], tuple[int, int]]:
        grid = [
            [
                Tile(), 
                Tile(), 
                Tile(), 
                Tile(reward=1, occupying=Tile.ENERGY, is_terminal=True)
            ],
            [
                Tile(), 
                Tile(occupying=Tile.OBSTACLE), 
                Tile(), 
                Tile(reward=-1, occupying=Tile.TROLL, is_terminal=True)
            ],
            [
                Tile(occupying=Tile.ROBOT), 
                Tile(), 
                Tile(), 
                Tile()
            ]
        ]
        return grid, (0, 2)

    def _copy_grid(self, grid: list[list[Tile]]) -> list[list[Tile]]:
        copied_grid = []
        for row in grid:
            copied_row = []
            for tile in row:
                copied_row.append(tile.copy())
            copied_grid.append(copied_row)
        return copied_grid
        
    def _illegal_action(self, action: Action) -> bool:
        new_x: int = self.robot_pos[0] + action[0]
        new_y: int = self.robot_pos[1] + action[1]
        if new_y >= len(self.grid):
            warn("* Illegal move down")
            return True
        if new_y < 0:
            warn("* Illegal move up")
            return True
        if new_x >= len(self.grid[0]):
            warn("* Illegal move right")
            return True
        if new_x < 0:
            warn("* Illegal move left")
            return True
        if self.grid[new_y][new_x].is_obstacle():
            warn("* Illegal move to obstacle")
            return True
        return False

    def _move_robot(self, grid: list[list[Tile]], direction: tuple[int, int]) -> tuple[int, int]:
        """ 
        Move robot's location on the grid to the new position
        
        Returns the robot's new location
        """
        new_x: int = self.robot_pos[0] + direction[0]
        new_y: int = self.robot_pos[1] + direction[1]
        old_x: int = self.robot_pos[0]
        old_y: int = self.robot_pos[1]
        grid[old_y][old_x].remove_robot()
        grid[new_y][new_x].add_robot()
        return new_x, new_y
        
    def handle_action(self, action: Action) -> State:
        """ Process the given action; Return the state to transition to """
        if self._illegal_action(action):
            return State(grid=self.grid, robot_pos=self.robot_pos)
        new_grid = self._copy_grid(self.grid)
        new_pos = self._move_robot(new_grid, action)
        return State(grid=new_grid, robot_pos=new_pos)
    
    def is_terminal(self) -> bool:
        """ Returns whether this state is a terminal state """
        return self.grid[self.robot_pos[1]][self.robot_pos[0]].is_terminal

class Model:
    """ Keeps track of the current game state and runs the main loop """
    def __init__(self):
        self.controller = ctrl.Controller()
        self.view = vw.View()
        self.cur_state = State()
        self.agent_controller = ag_ctrl.AgentController()
        self.agent = ag.Agent(self.agent_controller)
        self.agent_sensors = ag_ss.AgentSensors(self.agent)
        self.simulating_game = False # Whether the agent simulation is in progress

    def _handle_inputs(self):
        if self.controller.should_step():
            if self.cur_state.is_terminal():
                warn("* Current state is terminal; please reset game")
                return
            self.agent_sensors.send_observations(self.cur_state)
            self.cur_state = self.cur_state.handle_action(self.agent_controller.get_action())
        elif self.controller.should_reset_game():
            self.cur_state = State()
        elif self.controller.should_simulate_game():
            if self.cur_state.is_terminal():
                warn("* Current state is terminal; please reset game")
                return
            self.simulating_game = True

    def _simulate_game(self):
        self.agent_sensors.send_observations(self.cur_state)
        self.cur_state = self.cur_state.handle_action(self.agent_controller.get_action())
        if self.cur_state.is_terminal():
            self.simulating_game = False

    def _update(self):
        self.view.update(self.cur_state)
        if not self.simulating_game:
            self.controller.update()
            self._handle_inputs()
        else:
            self._simulate_game()

    def run(self):
        """ Run the game loop """
        while not self.controller.should_quit():
            self._update()

def main():
    model = Model()
    model.run()

if __name__ == "__main__":
    main()