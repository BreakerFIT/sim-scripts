#!/usr/bin/python

from __future__ import print_function
from datetime import datetime
from argparse import ArgumentParser
import os
import re
import subprocess
import sys

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)


def parse_arguments():
    unlimited_funds = '30000'

    parser = ArgumentParser(description='Make optimized deck for a mission.')
    parser.add_argument('member', metavar='MEMBER', help='member to sim for')
    parser.add_argument('mission', metavar='MISSION', help='mission to sim')
    parser.add_argument('-f', dest='funds', action='store_const', const=unlimited_funds, default='0', help='use unlimited SP (default: use no SP)')
    parser.add_argument('-e', dest='bge', metavar='BGE', default='', help='Use BGE as battleground effect (default: none)')
    args = parser.parse_args()

    return (args.member, args.mission, args.funds, args.bge)


def test_and_get_optimized_deck(command):
    print('RUNNING: ' + command)
    sim_proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, close_fds=True)
    while True:
        try:
            line = sim_proc.stdout.readline()
        except KeyboardInterrupt:
            break 
        if not line:
            break
        
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

mission_sim_iter = 10000

def mission_params(funds, bge):
    return '-r -e "' + bge + '" fund ' + funds + ' '

def format_mission_results(member, mission, funds, bge, result):
    funded_string = 'unfunded' if funds == '0' else 'funded'
    bge_string = bge if bge == '' else 'no BGE'
    result_string = 'MISSION: ' + mission + ' for ' + member + ' (' + funded_string + ', ' + bge_string + '): ' + result

    return result_string

def test_mission(member, mission, funds, bge):
    params = mission_params(funds, bge)

    climb_command = make_climb_command(member, member, mission, params, mission_sim_iter)
    start_date = datetime.now()
    (climb_line, climb_deck) = test_and_get_optimized_deck(climb_command)

    reorder_command = make_climb_command(member, climb_deck, mission, params, mission_sim_iter)
    (reorder_line, reorder_deck) = test_and_get_optimized_deck(reorder_command)
    end_date = datetime.now()

    print('[Sim took: ' + str(end_date - start_date) + ']')
    print('')
    results = format_mission_results(member, mission, funds, bge, reorder_line)
    print(results)

(member, mission, funds, bge) = parse_arguments()
test_mission(member, mission, funds, bge)
