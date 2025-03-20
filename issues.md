# Closed

1. Create game loop
2. Allow user to quit from game loop

# Open

3. Create state representation

# Backlog

## Class Structure
* Model
    - Contains current game state
    - Contains game loop
    - Pygame agnostic (should not require pygame)
    - Log current game state from a given action (optional)
* View
    - Display game
    - Choose either to display using terminal or pygame
    - Make window scalable (optional)
* Controller
    - Handle user input from terminal
    - Handle user input from pygame gui (optional)
* AgentSensors
    - Ferry information from the model to the agent
* AgentController
    - Ferry information from the agent to the model
* Agent
    - Make decisions based on agent sensor input
    - Update learned values
    - Send action to agent controller
