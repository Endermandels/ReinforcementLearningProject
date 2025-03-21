# ReinforcementLearningProject

## Description

Program a robot using reinforcement learning to move through
a grid based world, seeking out energy spaces
and avoiding trolls.

## Running

Run the model.py file:

    python3 model.py

TODO: Add arguments to run in terminal or with pygame

## Terminal

### Terminal Controls

All terminal controls are listed after running model.py:

    1. quit - Quit the program
    2. reset game - Reset the game state to the default state
    3. step through next agent action - Allow the agent to make one action
    4. simulate agent playing - Allow the agent to make actions until a terminal state is reached

### Terminal View

Each grid tile is represented by colored characters.
Below is a description of what each colored character represents:

    cyan '@' - Robot
    white '.' - Robot can move through this space
    yellow '#' - Robot cannot move through this space
    green '$' - Energy space (positive reward)
    red '!' - Troll space (negative reward)
    bold - Terminal space

## Pygame

TODO