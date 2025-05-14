import argparse
import itertools
import subprocess
from urllib.parse import urlsplit
import heapq

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

def banner():
     print(f"""{ORANGE}

██╗  ██╗ █████╗ ███████╗██╗  ██╗██████╗ ██████╗  ██████╗ ██╗    ██╗███╗   ██╗███████╗
██║  ██║██╔══██╗██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║████╗  ██║██╔════╝
███████║███████║███████╗███████║██████╔╝██████╔╝██║   ██║██║ █╗ ██║██╔██╗ ██║███████╗
██╔══██║██╔══██║╚════██║██╔══██║██╔══██╗██╔══██╗██║   ██║██║███╗██║██║╚██╗██║╚════██║
██║  ██║██║  ██║███████║██║  ██║██████╔╝██║  ██║╚██████╔╝╚███╔███╔╝██║ ╚████║███████║
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝
                                                                                     

""")

leet_map = {
    'a': ['a', 'A', '@', '4'],
    'e': ['e', 'E', '3'],
    'i': ['i', 'I', '1', '!'],
    'o': ['o', 'O', '0'],
    's': ['s', 'S', '$', '5'],
    't': ['t', 'T', '7']
}
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"{BOLD_RED}Error executing command: {e}{RESET}")
        return ""
    
def top_keys(dictionary, n=15):
    if not dictionary:
        return []
    return heapq.nlargest(n, dictionary, key=dictionary.get)

def main():
    try:
        banner()
        parser = argparse.ArgumentParser(description="Domain Enumeration and Recon Tool")
        parser.add_argument('-u', '--url', help='Target URL')
        args = parser.parse_args()

        if args.url:
            counter = {}

            domain = urlsplit(args.url).netloc
            run_command(f"cewl -w {domain}.txt {args.url}")

            with open(f'{domain}.txt', 'r') as f:
                words = [line.strip() for line in f.readlines()]
                for word in words:
                    word = word.lower()
                    if word.lower not in counter:
                        counter[word] = 0
                    counter[word] += 1
            print(top_keys(counter))

    except KeyboardInterrupt:
        print(f"\n{BOLD_RED}Interupted by user ")

main()