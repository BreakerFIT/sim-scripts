#!/usr/bin/python

from __future__ import print_function
from datetime import datetime
from argparse import ArgumentParser
import re
import subprocess
import simlib.output

def parse_arguments():
    unlimited_funds = '30000'

    parser = ArgumentParser(description='Make optimized PVP surge decks (requires ECG gauntlets).')
    parser.add_argument('member', metavar='MEMBER', help='member to sim for')
    parser.add_argument('-f', dest='funds', action='store_const', const=unlimited_funds, default='0', help='use unlimited SP (default: use no SP)')
    parser.add_argument('-e', dest='bge', metavar='BGE', default='', help='Use BGE as battleground effect (default: none)')
    args = parser.parse_args()

    return (args.member, args.funds, args.bge)


def test_and_get_optimized_deck(command, detail_log):
    print('RUNNING: ' + command)
    sim_proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, close_fds=True)
    while True:
        try:
            line = sim_proc.stdout.readline()
        except KeyboardInterrupt:
            break 
        if not line:
            break
        
        print(line, file=detail_log, end='', sep='')

        if 'units:' in line:
            print('.', end='', sep='')
        if line.startswith('Optimized Deck:'):
            print('')
            line = re.sub('Optimized Deck: ', '', line)
            line = re.sub('\n', '', line)
            deck_only = re.sub('.*:', '', line)

            return (line, deck_only)

def make_climb_command(member, deck, target, params, count):
    command = './tuo ' + '"' + deck + '"' + ' "' + target + '" -t 32 -o="data/' + member + '.txt" ' + params + ' endgame 1 climb ' + str(count)
    return command

def make_reorder_command(member, deck, target, params, count):
    command = './tuo ' + '"' + deck + '"' + ' "' + target + '" -t 32 -o="data/' + member + '.txt" ' + params + ' endgame 1 reorder ' + str(count)
    return command

pvp_sim_iter = 2000

def pvp_atk_params(funds, bge):
    return '-r -s -e "' + bge + '" fund ' + funds + ' '

def pvp_def_params(funds, bge):
    return 'enemy:ordered -e "' + bge + '" fund ' + funds + ' '

def format_pvp_results(type, member, gauntlet, funds, bge, result):
    funded_string = 'unfunded' if funds == '0' else 'funded'
    bge_string = bge if bge != '' else 'no BGE'
    result_string = 'PVP SURGE ' + type + ' (' + gauntlet + ') for ' + member + ' (' + funded_string + ', ' + bge_string + '): ' + result

    return result_string

def format_pvp_atk_results(*args):
    return format_pvp_results('ATTACK', *args)

def format_pvp_def_results(*args):
    return format_pvp_results('DEFENSE', *args)

def test_surge(member, funds, bge, detail_log):
    gauntlets = ["ECG_1000", "ECG_500", "ECG_100"]
    params = pvp_atk_params(funds, bge)

    last_deck = member
    start_date = datetime.now()

    for gauntlet in gauntlets:
        last_gauntlet = gauntlet

        climb_command = make_climb_command(member, last_deck, gauntlet, params, pvp_sim_iter)
        (climb_line, climb_deck) = test_and_get_optimized_deck(climb_command, detail_log)

        reorder_command = make_reorder_command(member, climb_deck, gauntlet, params, pvp_sim_iter)
        (last_line, last_deck) = test_and_get_optimized_deck(reorder_command, detail_log)

        win_rate_str = re.match('.*units: (.*):.*', last_line).group(1)
        win_rate = float(win_rate_str)
        if win_rate < 60:
            break

    params = pvp_def_params(funds, bge)
    climb_command = make_climb_command(member, last_deck, last_gauntlet, params, pvp_sim_iter)
    (def_line, def_deck) = test_and_get_optimized_deck(climb_command, detail_log)

    end_date = datetime.now()

    print('[Sim took: ' + str(end_date - start_date) + ']')
    print('')
    atk_results = format_pvp_atk_results(member, last_gauntlet, funds, bge, last_line)
    print(atk_results)
    def_results = format_pvp_def_results(member, last_gauntlet, funds, bge, def_line)
    print(def_results)

def pvp_ecg_logfiles(member, funds, bge):
    bge_suffix = '-' + bge if bge else ''
    suffix = '-pvp-ecg-' + funds + 'sp' + bge_suffix + '.txt'
    return (member + suffix, member + '-log' + suffix)

(member, funds, bge) = parse_arguments()
detail_log = simlib.output.prep_output(*pvp_ecg_logfiles(member, funds, bge))
test_surge(member, funds, bge, detail_log)
