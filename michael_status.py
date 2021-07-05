"""
Helper script to check the status of nodes in Michael
"""

import os
from tabulate import tabulate

__author__ = "pzarabadip"
__version__ = "0.1"
__maintainer__ = "Pezhman Zarabadi-Poor"
__email__ = "pzarabadip@gmail.com"
__status__ = "Development"
__date__ = "February 2021"

username = os.environ['USER']

os.system('nodetypes > nodes.txt')

with open('./nodes.txt', mode='r') as fhandler:
    lines = fhandler.readlines()

for line in lines:
    if 'type A nodes' in line:
        sp = line.split()
        TOTAL_A_NODES = int(sp[0])

    if 'type K nodes' in line:
        sp = line.split()
        TOTAL_K_NODES = int(sp[0])
        
TOTAL_A_CORES = TOTAL_A_NODES * 40
TOTAL_K_CORES = TOTAL_K_NODES * 24

os.system('qstat -u "*" > qstat.txt')

with open('./qstat.txt', mode='r') as fhandler:
    lines = fhandler.readlines()

k_core_count = 0
user_k_count = 0
a_core_count = 0
user_a_count = 0

for index, line in enumerate(lines):
    if index > 2:
        spl = line.split()
        status = spl[4]
        if status in ['r','Rr']:
            node_type = spl[7].split('-')[1]
            if node_type.startswith('a'):
                a_core_count += int(spl[8])
                if spl[3] == username:
                    user_a_count += int(spl[8])
            elif node_type.startswith('k'):
                k_core_count += int(spl[8])
                if spl[3] == username:
                    user_k_count += int(spl[8])

os.system('rm -rf qstat.txt nodes.txt')

print('\n')
print(tabulate(
    [
        ['A nodes',TOTAL_A_NODES,TOTAL_A_CORES,a_core_count,user_a_count],
        ['K nodes',TOTAL_K_NODES,TOTAL_K_CORES,k_core_count,user_k_count]
    ],
    headers = ['Node Type','Total Number of Nodes', 'Total Number of Cores', 'Number of Running Cores', 'User Running Cores']
))
print('\n')


