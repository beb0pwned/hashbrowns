import os
import re
import argparse
import itertools

# COLORS
GREEN = "\033[92m"
RED = "\033[91m"
TEAL = "\033[96m"
MAGENTA = "\033[95m"
ORANGE = "\033[93m"
BOLD_ORANGE = "\033[1;93m"
RESET = "\033[0m"
BOLD_GREEN = "\033[1;92m"
BOLD_RED = "\033[1;91m"
BOLD_MAGENTA = "\033[1;95m"
BOLD_TEAL = "\033[1;96m"

leet_map = {
    'a': ['a', 'A', '@', '4'],
    'e': ['e', 'E', '3'],
    'i': ['i', 'I', '1', '!'],
    'o': ['o', 'O', '0'],
    's': ['s', 'S', '$', '5'],
    't': ['t', 'T', '7']
}


def main():
    try: 

        parser = argparse.ArgumentParser(description="Domain Enumeration and Recon Tool")
        parser.add_argument('-u', '--url', help='Target URL')

    except:
        pass