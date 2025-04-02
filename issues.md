# Closed

1. Create game loop
2. Allow user to quit from game loop
3. Create state representation
4. Create Agent
5. Simulate agent playing the game
6. Show statistics
7. Specify Agent controller during initialization
8. Make Tile and State class immutable
9. Create pygame view and controller
10. Create resizable grid
11. Handle pygame inputs to run the game
12. Display stats to pygame window
13. Create config file
14. Create pygame handler
15. Create sleep option to slow down simulation
16. Keep track of state rewards
17. Create RL agent

# Open

18. Create training and test simulations

# Backlog

- Show warning messages in pygame view
- Create detached version (i.e. no Controller or View)

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
