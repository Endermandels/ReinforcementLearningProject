class BColors:
    """ Text colors """
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    HEADER = '\033[95m'
    ENDC = '\033[0m'

def cprint(string: str, col: BColors = BColors.ENDC):
    """ Print string with specified color """
    print(f"{col}{string}{BColors.ENDC}")

def warn(string: str):
    """ Print a warning string """
    print(f"{BColors.BOLD}{BColors.YELLOW}{string}{BColors.ENDC}")