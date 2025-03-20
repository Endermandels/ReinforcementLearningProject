class bcolors:
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

def cprint(string: str, col: bcolors = bcolors.ENDC):
    """ Print string with specified color """
    print(f"{col}{string}{bcolors.ENDC}")

def warn(string: str):
    """ Print a warning string """
    print(f"{bcolors.BOLD}{bcolors.YELLOW}{string}{bcolors.ENDC}")