###TODO: Add option for leetspeak; User-Agent Header; custom wordlist instead of crawling the webpage, custom blacklist

import argparse
from itertools import product
import subprocess
from urllib.parse import urlsplit
import heapq
import gzip
import os

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
    '''Runs a system command'''
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"{BOLD_RED}Error executing command: {e}{RESET}")
        return ""
    
def top_keys(dictionary, n):
    '''Checks the most common words in a dictionary'''
    if not dictionary:
        return []
    return heapq.nlargest(n, dictionary, key=dictionary.get)

def generate_lists(filename, words, args):
    '''Write combinations and variants to file.'''
    with open(filename, 'w') as f:
        for word in words:
            for i in range(0, 100001):
                f.write(f"{word}{i}\n")
                f.write(f"{word}{i:06}\n")
                if args.symbols:
                    for sym in symbols:
                        f.write(f"{word}{i}{sym}\n")
                        f.write(f"{word}{i:06}{sym}\n")
        # combine pairs
        for combo in product(words, repeat=2):
            base = ''.join(combo)
            for i in range(0, 100001):
                f.write(f"{base}{i}\n")
                f.write(f"{base}{i:06}\n")
                if args.symbols:
                    for sym in symbols:
                        f.write(f"{base}{i}{sym}\n")
                        f.write(f"{base}{i:06}{sym}\n")
            f.write(f"{base}\n")

def main():
    try:
        banner()
        parser = argparse.ArgumentParser(description="Custom Password List Generator")

        parser.add_argument(
            '-u', '--url', 
            help='Target URL'
            )
        parser.add_argument(
            '-c', '--check', 
            action='store_true', 
            help='Check the top words of a website'
            )
        parser.add_argument(
            '-b', '--blacklist', 
            type=lambda s: [w.strip().lower() for w in s.split(',')],
            default=[], 
            help='Comma-separated words to blacklist from wordlist (e.g. "squarespace,community")',
                            )
        parser.add_argument(
            '-n','--top', 
            help="Top 'N' words from (default: 5)",
            type=int,
            default=5
        )
        parser.add_argument(
            '-s','--symbols',
            help="Toggle to add symbols to the end of the word",
            action='store_true',
        )
        parser.add_argument(
            '-g', '--gzip',
            help='Gzip compress final wordlist',
            action='store_true'
        )
        parser.add_argument(
            '-w', '--words',
            help='Comma-separated words to create a password list from. Cannot be used with -u',
            default= [],
            type=lambda s: [w.strip() for w in s.split(',')]
        )
        args = parser.parse_args()
        blacklist = args.blacklist


        if args.url and args.words:
            parser.error('Cannot use --url and --words together.')

        if args.url:

            domain = urlsplit(args.url).netloc
            print(f"{TEAL}[+] Crawling {args.url}...{RESET}")
            run_command(f"cewl -m 5 -w {domain}.txt {args.url}")
            source_file = f"{domain}.txt"
            with open(source_file, 'r') as f:
                raw_words = [line.strip() for line in f]
        else:
            source_file = 'custom.txt'
            raw_words = args.words

        # Build counter with blacklist filtering
        counter = {}
        for w in raw_words:
            if any(b in w.lower() for b in blacklist):
                continue
            for variant in (w.lower(), w.upper(), w.title()):
                counter[variant] = counter.get(variant, 0) + 1

        most_common = top_keys(counter, n=(args.top * (3 if args.url else 1)))

        if args.url and args.check:
            display = most_common[2::3] if args.url else most_common
            print(f"{GREEN}[!] Top Words: {', '.join(display)}{RESET}")
            return

        # Generate output
        print(f"{TEAL}[+] Generating wordlist...{RESET}")
        generate_lists(source_file, most_common, args)



        if args.gzip:
            print(f"{TEAL}[+] Compressing to {domain}.txt.gz...{RESET}")
            with open(f'{domain}.txt', 'rb') as f_in, gzip.open(f"{domain}.txt.gz", 'wb') as f_out:
                f_out.writelines(f_in)
            if os.path.exists(f'{domain}.txt'):
                os.remove(f'{domain}.txt')
            print(f"{GREEN}[+] Compression complete{RESET}")

        print(f"{GREEN}[+] Done!{RESET}")
                    
    except KeyboardInterrupt:
        print(f"\n{BOLD_RED}Interupted by user ")
              
if __name__ == "__main__":
    main()