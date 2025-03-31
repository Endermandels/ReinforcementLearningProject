from __future__ import annotations
from toolbox import warn, error
from typing import NamedTuple
from enum import Enum

MOVE_REWARD = -0.04

class Stats:
    """ Stats collected while running the model """
    def __init__(self):
        self.num_iterations: int  = 0 # Number of iterations (includes illegal actions)
        self.num_actions: int = 0 # Number of successful actions
        self.reward: int = 0

class Action(Enum):
    """ Available actions """
    UP = (0,-1)
    DOWN = (0,1)
    LEFT = (-1,0)
    RIGHT = (1,0)

class TileSpace(Enum):
    """ What can occupy a tile space """
    OBSTACLE = '#'
    ROBOT = '@'
    OPEN = '.'
    ENERGY = '$'
    TROLL = '!'

class Tile(NamedTuple):
    reward: int = 0
    occupying: TileSpace = TileSpace.OPEN
    is_terminal: bool = False

class State(NamedTuple):
    grid: list[list[Tile]]
    robot_pos: tuple[int, int] # x and y location of robot
    reward: int = 0
    is_terminal: bool = False

def copy_grid(grid: list[list[Tile]]) -> list[list[Tile]]:
    copied_grid = []
    for row in grid:
        copied_row = []
        for tile in row:
            copied_row.append(Tile(tile.reward, tile.occupying, tile.is_terminal))
        copied_grid.append(copied_row)
    return copied_grid

def get_robot_pos(grid: list[list[Tile]]) -> tuple[int, int]:
    # NOTE: UNUSED
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if tile.occupying == TileSpace.ROBOT:
                return x, y
    error("!!! Robot not found")
    return -1, -1

def is_illegal_action(state: State, action: Action) -> bool:
    grid = state.grid
    robot_pos = state.robot_pos
    new_x: int = robot_pos[0] + action.value[0]
    new_y: int = robot_pos[1] + action.value[1]
    if new_y >= len(grid):
        warn("* Illegal move down")
        return True
    if new_y < 0:
        warn("* Illegal move up")
        return True
    if new_x >= len(grid[0]):
        warn("* Illegal move right")
        return True
    if new_x < 0:
        warn("* Illegal move left")
        return True
    if grid[new_y][new_x].occupying == TileSpace.OBSTACLE:
        warn("* Illegal move to obstacle")
        return True
    return False

def move_robot(state: State, direction: tuple[int, int]) -> State:
    """ Move robot's location on the grid to the new position; Return the new State """
    grid = copy_grid(state.grid)
    robot_pos = state.robot_pos
    old_x = robot_pos[0]
    old_y = robot_pos[1]
    new_x = old_x + direction[0]
    new_y = old_y + direction[1]
    new_tile = grid[new_y][new_x] 
    grid[old_y][old_x] = Tile()
    grid[new_y][new_x] = Tile(reward=new_tile.reward, occupying=TileSpace.ROBOT, 
                              is_terminal=new_tile.is_terminal)
    return State(grid, (new_x, new_y), new_tile.reward + MOVE_REWARD, new_tile.is_terminal)
    
def handle_action(state: State, action: Action) -> State:
    """ Process the given action; Returns the new state or the same state on an illegal action """
    if is_illegal_action(state, action):
        return state
    new_state = move_robot(state, action.value)
    return new_state
