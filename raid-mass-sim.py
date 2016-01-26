#!/usr/bin/python

from __future__ import print_function
import subprocess
from argparse import ArgumentParser
import re
from datetime import datetime
import simlib.opt
import simlib.output

decks_file = "data/customdecks.txt"
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

def parse_arguments():
    parser = ArgumentParser(description='Make optimized raid decks (requires ECG gauntlets). Also logs results to results directory.')
    parser.add_argument('guild', metavar='GUILD', help='guild gauntlet to sim for')
    parser.add_argument('raid', metavar='RAID', help='raid to sim against')
    parser.add_argument('-yf', dest='forts', metavar='FORTS', default='', help='Use FORTS as attacking fortresses (default: none)')
    parser.add_argument('-e', dest='bge', metavar='BGE', default='', help='Use BGE as battleground effect (default: none)')
    args = parser.parse_args()

    return (args.guild, args.raid, args.bge, args.forts)

def raid_params(bge, fort):
    return '-r -e "' + bge + '" yfort "' + fort + '"'

def raid_name(raid, level):
    return raid + '-' + str(level)

def test_raid(member, raid, bge, fort, summaryfile):
    params = raid_params(bge, fort)
    level_14_command = simlib.opt.climb_command(member, member, raid_name(raid, 14), params, 2000)
    start_date = datetime.now()
    (level_14_line, level_14_deck) = simlib.opt.optimize(level_14_command)
    end_date = datetime.now()

    print("")
    print("[Sim took: " + str(end_date - start_date) + "]")
    print("LEVEL 14 DECK for " + member + ": " + level_14)
    print("")

    level_19_command = simlib.opt.climb_command(member, level_14_deck, raid_name(raid, 19), params, 2000)
    start_date = datetime.now()
    (level_19_line, level_19_deck) = simlib.opt.optimize(level_19_command)
    end_date = datetime.now()

    print("")
    print("[Sim took: " + str(end_date - start_date) + "]")
    print("LEVEL 19 DECK for " + member + ": " + level_19)
    print("")

    level_25_command = simlib.opt.climb_command(member, level_19_deck, raid_name(raid, 25), params, 2000)
    start_date = datetime.now()
    (level_25_line, level_25_deck) = simlib.opt.optimize(level_25_command)
    end_date = datetime.now()

    print("")
    print("[Sim took: " + str(end_date - start_date) + "]")
    print("LEVEL 25 DECK for " + member + ": " + level_25)
    print("")

    print("LEVEL 14 DECK for " + member + ": " + level_14, file=summaryfile)
    print("LEVEL 19 DECK for " + member + ": " + level_19, file=summaryfile)
    print("LEVEL 25 DECK for " + member + ": " + level_25, file=summaryfile)
    print("", file=summaryfile)

def mass_raid_ecg_logfile(guild, raid, bge, forts):
    bge_suffix = '-' + bge if bge else ''
    return guild + '-mass-raid-ecg-' + raid + '-' + bge_suffix + '-' + forts + '.txt'

(guild, raid, bge, forts) = parse_arguments()
fname = mass_raid_ecg_logfile(guild, raid, bge, forts)
simlib.output.prep_output(fname)

summary_fname = re.sub('-', '-summary-', fname, count=1)
summaryfile = open('results/' + summary_fname, 'w', 1)

members = get_members(guild)
print(members)

for member in members:
    test_raid(member, raid, bge, forts, summaryfile)
