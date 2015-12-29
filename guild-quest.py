#!/usr/bin/python

from __future__ import print_function
from datetime import datetime
from argparse import ArgumentParser
import simlib.output
import simlib.opt

def parse_arguments():
    unlimited_funds = '30000'

    parser = ArgumentParser(description='Make optimized deck for a guild quest. Also logs results to results directory.')

    parser.add_argument('member', metavar='MEMBER', help='member to sim for')
    parser.add_argument('mission', metavar='MISSION', help='mission to sim')
    parser.add_argument('guild_forts', metavar='GUILD_FORTS', help="the guild's current forts")
    parser.add_argument('enemy_forts', metavar='ENEMY_FORTS', help="the enemy's current forts")
    parser.add_argument('-f', dest='funds', action='store_const', const=unlimited_funds, default='0', help='use unlimited SP (default: use no SP)')
    parser.add_argument('-e', dest='bge', metavar='BGE', default='', help='Use BGE as battleground effect (default: none)')

    args = parser.parse_args()

    return (args.member, args.mission, args.guild_forts, args.enemy_forts, args.funds, args.bge)

gq_sim_iter = 10000

def gq_params(guild_forts, enemy_forts, funds, bge):
    return '-r -e "' + bge + '" fund ' + funds + ' yfort "' + guild_forts + '" efort "' + enemy_forts + '" '

def format_gq_results(member, mission, guild_forts, enemy_forts, funds, bge, result):
    funded_string = 'unfunded' if funds == '0' else 'funded'
    bge_string = bge if bge != '' else 'no BGE'
    result_string = 'GUILD QUEST: ' + mission + ' (' + enemy_forts+ ') for ' + member + ' (' + funded_string + ', ' + bge_string + '): ' + result

    return result_string

def test_gq(member, mission, guild_forts, enemy_forts, funds, bge):
    params = gq_params(guild_forts, enemy_forts, funds, bge)

    climb_command = simlib.opt.climb_command(member, member, mission, params, gq_sim_iter)
    start_date = datetime.now()
    (climb_line, climb_deck) = simlib.opt.optimize(climb_command)

    reorder_command = simlib.opt.reorder_command(member, climb_deck, mission, params, gq_sim_iter)
    (reorder_line, reorder_deck) = simlib.opt.optimize(reorder_command)
    end_date = datetime.now()

    print('[Sim took: ' + str(end_date - start_date) + ']')
    print('')
    results = format_gq_results(member, mission, guild_forts, enemy_forts, funds, bge, reorder_line)
    print(results)

def gq_logfiles(member, mission, guild_forts, enemy_forts, funds, bge):
    bge_suffix = '-' + bge if bge else ''
    return member + '-gq-' + mission + '-' + guild_forts + '-' + enemy_forts + '-' + funds + 'sp' + bge_suffix + '.txt'

(member, mission, guild_forts, enemy_forts, funds, bge) = parse_arguments()
simlib.output.prep_output(gq_logfiles(member, mission, guild_forts, enemy_forts, funds, bge))
test_gq(member, mission, guild_forts, enemy_forts, funds, bge)
