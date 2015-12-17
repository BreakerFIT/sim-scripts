#!/usr/bin/python

from __future__ import print_function
import subprocess
import re
import sys
import os
import re
from datetime import datetime

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

decks_file = "data/customdecks.txt"

def test_and_get_optimized_deck(command):
    print("RUNNING: " + command)
    sim_proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, close_fds=True)
    while True:
        try:
            line = sim_proc.stdout.readline()
        except KeyboardInterrupt:
            break 
        if not line:
            break
        
        if "units:" in line:
            print(".", end='', sep='')
        if line.startswith("Optimized Deck:"):
            line = re.sub("\n", "", line)
            return line

def make_climb_command(member, deck, raid, level, params):
    command = './tuo ' + '"' + deck + '"' + ' "' + raid + '-' + str(level) + '" -t 16 -o="data/' + member + '.txt" ' + params + ' endgame 1 fund 0 climb 2000'
    return command

def test_raid(member, raid, bge, fort):
    params = '-r -e "' + bge + '" yfort "' + fort + '"'
    level_14_command = make_climb_command(member, member, raid, 14, params)
    start_date = datetime.now()
    level_14 = test_and_get_optimized_deck(level_14_command)
    end_date = datetime.now()

    print("")
    print("[Sim took: " + str(end_date - start_date) + "]")
    print("LEVEL 14 DECK for " + member + ": " + level_14)
    print("")

    level_14_deck = re.sub(".*:", "", level_14)
    level_19_command = make_climb_command(member, level_14_deck, raid, 19, params)
    start_date = datetime.now()
    level_19 = test_and_get_optimized_deck(level_19_command)
    end_date = datetime.now()

    print("")
    print("[Sim took: " + str(end_date - start_date) + "]")
    print("LEVEL 19 DECK for " + member + ": " + level_19)
    print("")

    level_19_deck = re.sub(".*:", "", level_19)
    level_25_command = make_climb_command(member, level_19_deck, raid, 25, params)
    start_date = datetime.now()
    level_25 = test_and_get_optimized_deck(level_25_command)
    end_date = datetime.now()

    print("")
    print("[Sim took: " + str(end_date - start_date) + "]")
    print("LEVEL 25 DECK for " + member + ": " + level_25)
    print("")


def get_members(gauntlet):
    members = []
    decks = open(decks_file, "r")
    for line in decks:
        if line.startswith(gauntlet + ":"):
            gauntlet_regexp = re.sub('.*: */(.*)/$', '\\1', line)
    decks.close()
    decks = open(decks_file, "r")
    for line in decks:
        if re.match(gauntlet_regexp, line):
            member = re.sub(':.*\n$', '', line)
            members.append(member)

    return members

grep_proc = subprocess.Popen("grep '^eca_.*' data/customdecks.txt | sed -e s/:.*$//", shell=True, stdout=subprocess.PIPE) 
members = grep_proc.stdout.read().splitlines()

guild = sys.argv[1]
raid = sys.argv[2]
bge = sys.argv[3]
forts = sys.argv[4]

members = get_members(guild)
print(members)

for member in members:
    test_raid(member, raid, bge, forts)
