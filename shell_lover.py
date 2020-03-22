#!/bin/python3
import sys
import os
import readline
import configparser
from optparse import OptionParser
from colorama import Fore, Back, Style
from os import environ

version="3.0"
author="r0ttenbeef"
pos="[" + Fore.GREEN + "+" + Fore.RESET + "] "
neg="[" + Fore.RED + "-" + Fore.RESET + "] "
prog="[" + Fore.BLUE + "*" + Fore.RESET + "] "
ps = Fore.RED + "♥" + Fore.GREEN + "shellz" + Fore.RED + "♥" + Fore.GREEN + ": " + Fore.RESET
confparse = configparser.ConfigParser()
class ShellList(object):
    def __init__(self, options):
        self.options = sorted(options)
    
    def complete(self, text, state):
        if state == 0:
            if not text:
                self.matches = self.options[:]
            else:
                self.matches = [s for s in self.options if s and s.startwith(text)]
        try:
            return self.matches[state]
        except IndexError:
            return None
    
    def display_matches(self, substitution, matches, longest_match_length):
        buffer = ""
        line_buffer = readline.get_line_buffer()
        columns = environ.get("COLUMNS", 80)
        print()
        tpl = "{:<" + str(int(max(map(len, matches)) * 1.2)) + "}"
        for match in matches:
            match = tpl.format(match[len(substitution):])
            if len(buffer + match) > columns:
                print(buffer)
                buffer = ""
            buffer += match
        if buffer:
            print(buffer)
        
        print(ps, end="")
        print(line_buffer, end="")
        sys.stdout.flush()

commands = ['help', 'exit', 'about', 'list', 'count', 'clear']
description = [
    'Show this help menu',
    'Exiting this prompt',
    'Show version',
    'List available shells',
    'Number of added shells',
    'Clear the screen, use ctrl+L'
]
commands = [x.split(' ')[0] for x in commands]
completer = ShellList(list(set(commands)))
readline.set_completer_delims(' \t\n;')
readline.set_completer(completer.complete)
readline.parse_and_bind('tab: complete')
readline.set_completion_display_matches_hook(completer.display_matches)

def welbanner():
    banner = """
    \t{0}┌─┐{1}┬ ┬┌─┐┬  ┬    {0}┬  {1}┌─┐┬  ┬┌─┐┬─┐
    \t{0}└─┐{1}├─┤├┤ │  │    {0}│  {1}│ │└┐┌┘├┤ ├┬┘
    \t{0}└─┘{1}┴ ┴└─┘┴─┘┴─┘  {0}┴─┘{1}└─┘ └┘ └─┘┴└─
    \t  {2}Reverse shell cheatsheet tool{1}
    \t  {2}Author{3} {4} {2}version{3} {5}
    """.format(Fore.RED, Fore.GREEN,Fore.CYAN, Fore.RESET, author, version)
    return banner

def shell_list():
    while True:
        cmd = str(input(ps))
        shellcount = len(confparse.sections())

        if (cmd in confparse.sections()):
            shell = dict(confparse[cmd])
            for key, val in shell.items():
                print(pos + Fore.YELLOW + cmd + " " + key + ": " + Fore.WHITE + val + Fore.RESET + "\n")

        elif (cmd == "exit") or (cmd == "quit") or (cmd == "q") or (cmd == "bye"):
            print(Fore.YELLOW + "bye.." + Fore.RESET)
            break

        elif (cmd == "") or (cmd == None):
            pass
        
        elif (cmd == commands[0]):
            for i in range(len(commands)):
                print(Fore.GREEN + commands[i] + "\n" + Fore.BLUE + "\t" + description[i] + Fore.RESET)
        
        elif (cmd == commands[2]):
            print(Fore.YELLOW + "This script is made with " + Fore.RED + "♥" + Fore.YELLOW + " by " + Fore.RESET + author + Fore.YELLOW + " version " + Fore.RESET + version)

        elif (cmd == commands[3]):
            print(pos + "{} shell types are loaded".format(shellcount))
            for i in range(shellcount):
                print(Fore.BLUE + str(i) + Fore.WHITE + ": " + Fore.MAGENTA + confparse.sections()[i] + Fore.RESET)

        elif (cmd == commands[4]):
            print(prog + "{} shell types ready and loaded".format(shellcount))
        
        elif (cmd == commands[5]):
            os.system('clear')

        else:
            print(neg + "Command not found, type 'help' for help menu.")
            pass
    return

def main():
    parser = OptionParser(usage="%prog [options]", version="%prog " + version)
    parser.add_option("-i", "--ip", dest="ip_addr", default=None, help="IP address to use with generated shell")
    parser.add_option("-p", "--port", dest="port", default=None, help="Port number that will connect back to your listener")
    (options, args) = parser.parse_args()
    if(options.ip_addr == None) or (options.port == None):
        parser.error("Required arguments are missing, use -h, --help for help menu.")
        sys.exit(1)
    confparse.read('shells.ini')
    confparse.set('DEFAULT', 'IPADDR', options.ip_addr)
    confparse.set('DEFAULT', 'PORT', options.port)
    print(welbanner())
    shell_list()

if __name__ == '__main__':
    main()