#!/usr/bin/python

from __future__ import print_function
from datetime import datetime
from argparse import ArgumentParser
import re
import subprocess
import simlib.output
import simlib.opt

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
    unlimited_funds = '30000'

    parser = ArgumentParser(description='Make optimized brawl decks (requires ECG gauntlets). Also logs results to results directory.')
    parser.add_argument('guild', metavar='GUILD', help='guild gauntlet to sim for')
    parser.add_argument('-f', dest='funds', action='store_const', const=unlimited_funds, default='0', help='use unlimited SP (default: use no SP)')
    parser.add_argument('-e', dest='bge', metavar='BGE', default='', help='Use BGE as battleground effect (default: none)')
    args = parser.parse_args()

    return (args.guild, args.funds, args.bge)

brawl_sim_iter = 1000

def brawl_atk_params(funds, bge):
    return '-r -s brawl -e "' + bge + '" fund ' + funds + ' '

def brawl_def_params(funds, bge):
    return 'enemy:ordered defense -e "' + bge + '" fund ' + funds + ' '

def format_brawl_results(type, member, gauntlet, funds, bge, result):
    funded_string = 'unfunded' if funds == '0' else 'funded'
    bge_string = bge if bge != '' else 'no BGE'
    result_string = 'BRAWL ' + type + ' (' + gauntlet + ') for ' + member + ' (' + funded_string + ', ' + bge_string + '): ' + result

    return result_string

def format_brawl_atk_results(*args):
    return format_brawl_results('ATTACK', *args)

def format_brawl_def_results(*args):
    return format_brawl_results('DEFENSE', *args)

def copy_cost(to_line, from_line):
    cost_match = re.match('.*units: \$([0-9]*).*', from_line)
    if cost_match:
        cost_str = cost_match.group(1)
        return re.sub('units: ', 'units: $' + cost_str + ' ', to_line)
    return to_line
    
def test_brawl(member, funds, bge):
    gauntlets = ["ECG_1000", "ECG_500", "ECG_100"]
    params = brawl_atk_params(funds, bge)

    last_deck = member
    start_date = datetime.now()

    for gauntlet in gauntlets:
        last_gauntlet = gauntlet

        climb_command = simlib.opt.climb_command(member, last_deck, gauntlet, params, brawl_sim_iter)
        (climb_line, climb_deck) = simlib.opt.optimize(climb_command)

        reorder_command = simlib.opt.reorder_command(member, climb_deck, gauntlet, params, brawl_sim_iter)
        (last_line, last_deck) = simlib.opt.optimize(reorder_command)

        last_line = copy_cost(last_line, climb_line)

        win_rate_str = re.match('.*units: [(](.*)% win.*', last_line).group(1)
        win_rate = float(win_rate_str)
        if win_rate < 60:
            break

    params = brawl_def_params(funds, bge)
    climb_command = simlib.opt.climb_command(member, last_deck, last_gauntlet, params, brawl_sim_iter)
    (def_line, def_deck) = simlib.opt.optimize(climb_command)

    end_date = datetime.now()

    print('[Sim took: ' + str(end_date - start_date) + ']')
    print('')
    atk_results = format_brawl_atk_results(member, last_gauntlet, funds, bge, last_line)
    print(atk_results)
    def_results = format_brawl_def_results(member, last_gauntlet, funds, bge, def_line)
    print(def_results)

def mass_brawl_ecg_logfile(guild, funds, bge):
    bge_suffix = '-' + bge if bge else ''
    return guild + '-mass-brawl-ecg-' + funds + 'sp' + bge_suffix + '.txt'


(guild, funds, bge) = parse_arguments()
simlib.output.prep_output(mass_brawl_ecg_logfile(guild, funds, bge))

members = get_members(guild)
print(members)

for member in members:
    test_brawl(member, funds, bge)
