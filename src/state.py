from __future__ import annotations
from toolbox import warn
from typing import NamedTuple
from enum import Enum

MOVE_REWARD = -0.04
ENERGY_REWARD = 1
TROLL_REWARD = -1

class Stats:
    """ Stats collected while running the model """
    def __init__(self):
        self.num_iterations: int  = 0 # Number of iterations (includes illegal actions)
        self.num_actions: int = 0 # Number of successful actions
        self.reward: float = 0.0

class Action(Enum):
    """ Available actions """
    UP = (0,-1)
    DOWN = (0,1)
    LEFT = (-1,0)
    RIGHT = (1,0)

class Tile(Enum):
    """ Static grid tiles """
    OBSTACLE = '#'
    OPEN = '.'

class MovableObject:
    ROBOT = '@'
    TROLL = '!'
    ENERGY = '$'

class State(NamedTuple):
    grid: tuple[tuple[Tile, ...], ...]
    robot_pos: tuple[int, int] # x and y location of robot
    troll_pos: tuple[int, int]
    energy_pos: tuple[int, int]
    reward: float = 0.0
    is_terminal: bool = False

# TODO: Encapsulate state as robot pos

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
    if grid[new_y][new_x] == Tile.OBSTACLE:
        warn("* Illegal move to obstacle")
        return True
    return False

def is_terminal_tile(state: State, pos: tuple[int, int]) -> bool:
    """ Return whether the tile at specified x, y position is terminal """
    return pos == state.energy_pos or pos == state.troll_pos

def get_tile_reward(state: State, pos: tuple[int, int]) -> float:
    """ Return tile reward at specified x, y position """
    if pos == state.troll_pos:
        return -1
    if pos == state.energy_pos:
        return 1
    return MOVE_REWARD

def move_robot(state: State, direction: tuple[int, int]) -> State:
    """ Move robot's location on the grid to the new position; Return the new State """
    robot_pos = state.robot_pos
    old_x = robot_pos[0]
    old_y = robot_pos[1]
    new_x = old_x + direction[0]
    new_y = old_y + direction[1]
    new_robot_pos = (new_x, new_y)
    
    return State(state.grid, 
                 new_robot_pos,
                 state.troll_pos,
                 state.energy_pos,
                 get_tile_reward(state, new_robot_pos),
                 is_terminal_tile(state, new_robot_pos))
    
def handle_action(state: State, action: Action) -> State:
    """ Process the given action; Returns the new state or the same state on an illegal action """
    if is_illegal_action(state, action):
        return state
    new_state = move_robot(state, action.value)
    return new_state
