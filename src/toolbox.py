from config import *

def cprint(string: str, col: BColors = BColors.ENDC):
    """ Print string with specified color """
    print(f"{col}{string}{BColors.ENDC}")

def warn(string: str):
    """ Print a warning string """
    print(f"{BColors.BOLD}{WARN_COL}{string}{BColors.ENDC}")
    
def error(string: str):
    """ Print an error string """
    print(f"{BColors.BOLD}{ERROR_COL}{string}{BColors.ENDC}")