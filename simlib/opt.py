
from __future__ import print_function
import re
import subprocess
from simlib import output
import sys

def optimize(command):
    print('RUNNING: ' + command)
    output.log('RUNNING: ' + command)
    sim_proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    while True:
        try:
            line = sim_proc.stdout.readline()
        except KeyboardInterrupt:
            break 
        if not line:
            break
        
        output.log(line, newline=False)

        if 'units:'.encode('UTF-8') in line:
            print('.', end='', sep='')
            sys.stdout.flush()
        if line.startswith('Optimized Deck:'.encode('UTF-8')):
            print('')
            line = re.sub('Optimized Deck: ', '', line.decode('UTF-8'))
            line = re.sub('\n', '', line)
            deck_only = re.sub('.*:', '', line)

            return (line, deck_only)

def climb_command(member, deck, target, params, count):
    command = 'cd .. & tuo ' + '"' + deck + '"' + ' "' + target + '" -t 32 -o="data/' + member + '.txt" ' + params + ' endgame 1 climb ' + str(count)
    return command

def reorder_command(member, deck, target, params, count):
    command = 'cd .. & tuo ' + '"' + deck + '"' + ' "' + target + '" -t 32 -o="data/' + member + '.txt" ' + params + ' endgame 1 reorder ' + str(count)
    return command
