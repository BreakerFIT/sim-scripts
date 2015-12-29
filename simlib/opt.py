
from __future__ import print_function
import re
import subprocess
from simlib import output

def optimize(command):
    print('RUNNING: ' + command)
    output.log('RUNNING: ' + command)
    sim_proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, close_fds=True)
    while True:
        try:
            line = sim_proc.stdout.readline()
        except KeyboardInterrupt:
            break 
        if not line:
            break
        
        output.log(line, newline=False)

        if 'units:' in line:
            print('.', end='', sep='')
        if line.startswith('Optimized Deck:'):
            print('')
            line = re.sub('Optimized Deck: ', '', line)
            line = re.sub('\n', '', line)
            deck_only = re.sub('.*:', '', line)

            return (line, deck_only)

def climb_command(member, deck, target, params, count):
    command = './tuo ' + '"' + deck + '"' + ' "' + target + '" -t 32 -o="data/' + member + '.txt" ' + params + ' endgame 1 climb ' + str(count)
    return command

def reorder_command(member, deck, target, params, count):
    command = './tuo ' + '"' + deck + '"' + ' "' + target + '" -t 32 -o="data/' + member + '.txt" ' + params + ' endgame 1 reorder ' + str(count)
    return command
