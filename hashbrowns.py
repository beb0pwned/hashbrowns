###TODO: Add option for leetspeak; User-Agent Header; gzip

import argparse
from itertools import product
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
                                                                                     

{RESET}""")

leet_map = {
        'a': ['4', '@'], 'b': ['8'], 'e': ['3'], 'g': ['6', '9'],
        'i': ['1', '!'], 'l': ['1', '|'], 'o': ['0'], 's': ['5', '$'],
        't': ['7', '+'], 'z': ['2']
    }

symbols = ['!', '@', '#', '$', '%','&','*', '?']

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"{BOLD_RED}Error executing command: {e}{RESET}")
        return ""
    
def top_keys(dictionary, n=36): # 12 words per variant ( 3 variants)
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
            print(f"{TEAL}[+] Grabbing most common words from {args.url}...{RESET}")
            run_command(f"cewl -m 5 -w {domain}.txt {args.url}")

            # Gets top 12 (36) most common words found on site
            with open(f'{domain}.txt', 'r+') as f:
                words = [line.strip() for line in f.readlines()]
                for word in words:
                    for variant in (word.lower(), word.upper(), word.title()):
                        counter[variant] = counter.get(variant, 0) + 1
                most_common_words = top_keys(counter)
                print(f'{GREEN}[!] Most Common Words: {', '.join(most_common_words)}{RESET}')

                print(f'{TEAL}[+] Generating Wordlist...{RESET}')
                # Combines 2 words
                for combo in product(most_common_words, repeat=2):    
                    for i in range(0, 100001):
                        for sym in symbols:
                            f.write(''.join(combo) + f'{i}' + sym +'\n')
                    for i in range(0, 100001):
                        for sym in symbols:
                            f.write(''.join(combo) + f'{i:06}' + sym + '\n')
                    f.write(''.join(combo) + '\n')
                    

                    
    except KeyboardInterrupt:
        print(f"\n{BOLD_RED}Interupted by user ")

main()