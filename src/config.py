class BColors:
    """ Text colors """
    BLACK = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

# Terminal colors
ROBOT_COL = BColors.CYAN
PAIN_COL = BColors.RED
REWARD_COL = BColors.GREEN
OBSTACLE_COL = BColors.YELLOW
OPEN_COL = BColors.ENDC

WARN_COL = BColors.YELLOW
ERROR_COL = BColors.RED
