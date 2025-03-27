# ReinforcementLearningProject

## Description

Program a robot using reinforcement learning to move through
a grid based world, seeking out energy spaces
and avoiding trolls.

## Running

Run the model.py file in terminal view:

    python3 model.py

Run the model.py file in pygame view:

    python3 model.py -p

## Terminal

### Terminal Controls

All terminal controls are listed after running model.py:

    1. quit - Quit the program
    2. reset game - Reset the game state to the default state
    3. step through next agent action - Allow the agent to make one action
    4. simulate agent playing - Allow the agent to make actions until a terminal state is reached

NOTE: Must reset game manually after reaching a terminal state.

### Terminal View

Each grid tile is represented by colored characters.
Below is a description of what each colored character represents:

    cyan '@' - Robot
    white '.' - Robot can move through this space
    yellow '#' - Robot cannot move through this space
    green '$' - Energy space (positive reward)
    red '!' - Troll space (negative reward)
    bold - Terminal space

On reaching a terminal state, the game stats will be displayed.

NOTE: You can configure the colors of the characters from the config.py file.

## Pygame

### Pygame Controls

All pygame controls are listed after running model.py:

    ESC/1 - Quit the program
    2 - Reset the game state to the default state
    3 - Step through next agent action
    4 - Simulate agent playing the game
    
NOTE: Must reset game manually after reaching a terminal state.

### Pygame View

Each grid tile is represented by a colored square.
Below is a description of what each colored square represents:

    cyan - Robot
    dark purple - Robot can move through this space
    yellow - Robot cannot move through this space
    green - Energy space (positive reward)
    red - Troll space (negative reward)
    white border - Terminal space

NOTE: Model stats are always displayed.