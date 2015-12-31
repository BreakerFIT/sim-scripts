#!/usr/bin/python

from __future__ import print_function
from datetime import datetime
from argparse import ArgumentParser
import re
import subprocess
import simlib.output
import simlib.opt

def parse_arguments():
    unlimited_funds = '30000'

    parser = ArgumentParser(description='Make optimized PVP surge decks (requires ECG gauntlets). Also logs results to results directory.')
    parser.add_argument('member', metavar='MEMBER', help='member to sim for')
    parser.add_argument('-f', dest='funds', action='store_const', const=unlimited_funds, default='0', help='use unlimited SP (default: use no SP)')
    parser.add_argument('-e', dest='bge', metavar='BGE', default='', help='Use BGE as battleground effect (default: none)')
    args = parser.parse_args()

    return (args.member, args.funds, args.bge)

pvp_sim_iter = 2000

def pvp_atk_params(funds, bge):
    return '-r -s -e "' + bge + '" fund ' + funds + ' '

def pvp_def_params(funds, bge):
    return 'enemy:ordered defense -e "' + bge + '" fund ' + funds + ' '

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

        climb_command = simlib.opt.climb_command(member, last_deck, gauntlet, params, pvp_sim_iter)
        (climb_line, climb_deck) = simlib.opt.optimize(climb_command, detail_log)

        reorder_command = simlib.opt.reorder_command(member, climb_deck, gauntlet, params, pvp_sim_iter)
        (last_line, last_deck) = simlib.opt.optimize(reorder_command, detail_log)

        win_rate_str = re.match('.*units: (.*):.*', last_line).group(1)
        win_rate = float(win_rate_str)
        if win_rate < 60:
            break

    params = pvp_def_params(funds, bge)
    climb_command = simlib.opt.climb_command(member, last_deck, last_gauntlet, params, pvp_sim_iter)
    (def_line, def_deck) = simlib.opt.optimize(climb_command, detail_log)

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
