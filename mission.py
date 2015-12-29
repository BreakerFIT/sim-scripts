#!/usr/bin/python

from __future__ import print_function
from datetime import datetime
from argparse import ArgumentParser
import simlib.output
import simlib.opt

def parse_arguments():
    unlimited_funds = '30000'

    parser = ArgumentParser(description='Make optimized deck for a mission. Also logs results to results directory.')

    parser.add_argument('member', metavar='MEMBER', help='member to sim for')
    parser.add_argument('mission', metavar='MISSION', help='mission to sim')
    parser.add_argument('-f', dest='funds', action='store_const', const=unlimited_funds, default='0', help='use unlimited SP (default: use no SP)')
    parser.add_argument('-e', dest='bge', metavar='BGE', default='', help='Use BGE as battleground effect (default: none)')

    args = parser.parse_args()

    return (args.member, args.mission, args.funds, args.bge)


mission_sim_iter = 10000

def mission_params(funds, bge):
    return '-r -e "' + bge + '" fund ' + funds + ' '

def format_mission_results(member, mission, funds, bge, result):
    funded_string = 'unfunded' if funds == '0' else 'funded'
    bge_string = bge if bge != '' else 'no BGE'
    result_string = 'MISSION: ' + mission + ' for ' + member + ' (' + funded_string + ', ' + bge_string + '): ' + result

    return result_string

def test_mission(member, mission, funds, bge, detail_log):
    params = mission_params(funds, bge)

    climb_command = simlib.opt.climb_command(member, member, mission, params, mission_sim_iter)
    start_date = datetime.now()
    (climb_line, climb_deck) = simlib.opt.optimize(climb_command, detail_log)

    reorder_command = simlib.opt.reorder_command(member, climb_deck, mission, params, mission_sim_iter)
    (reorder_line, reorder_deck) = simlib.opt.optimize(reorder_command, detail_log)
    end_date = datetime.now()

    print('[Sim took: ' + str(end_date - start_date) + ']')
    print('')
    results = format_mission_results(member, mission, funds, bge, reorder_line)
    print(results)

def mission_logfiles(member, mission, funds, bge):
    bge_suffix = '-' + bge if bge else ''
    suffix = '-mission-' + mission + '-' + funds + 'sp' + bge_suffix + '.txt'
    return (member + suffix, member + '-log' + suffix)

(member, mission, funds, bge) = parse_arguments()
detail_log = simlib.output.prep_output(*mission_logfiles(member, mission, funds, bge))
test_mission(member, mission, funds, bge, detail_log)
