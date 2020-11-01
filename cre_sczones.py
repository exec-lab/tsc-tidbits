#!/usr/bin/env python3
import os
import sys
import time
import csv
import socket
import ipaddress
from operator import itemgetter, attrgetter
from ipaddress import *
from tenable.sc import TenableSC

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

"""
Put access key in file called acc.key.  Just the key, one line. Don't press enter, just save.
Put secret key in a file called sec.key.  Just the key, one line.
The next 2 lines read your access and secret keys so you don't have to expose them in your code.
"""

accesskey = open('adm_acc.key').read().strip()
secretkey = open('adm_sec.key').read().strip()

sc = TenableSC('127.0.0.1', port=8443)
sc.login(access_key = accesskey, secret_key = secretkey)

crezones = {}
num_lines = 0
#num_flds = 0
num_zones = 0
num_passes = 0
#izonename = ''
iprange = ''

filetouse = sys.argv[1]

f = open(filetouse)
zonefile = csv.reader(f)
num_lines = len(f.readlines())
f.seek(0.0)

if num_lines == 0:
    print('\n')
    print('startzones.csv is empty...\n')

elif num_lines > 0:
    i = 0

    for row in zonefile:
        if num_lines == 0:
            break
        elif i == 0:
            num_zones = 1
            zonename = row[0]
            iprange = row[1]
            i += 1
        elif i > 0 and zonename == row[0]:
            iprange = iprange+','+row[1]
            i += 1        
        elif i > 0 and zonename != row[0]:
            num_passes += 1
#            print(zonename, 'Line 56.  passes =',num_passes, '  num_zones =',num_zones, 'i =', i, '\n')
#            print(iprange, '\n')
            crezones[num_zones] = {'zonename':zonename, 'iprange':iprange}
            num_zones += 1
            zonename = row[0]
            iprange = row[1]
            i += 1        
        if i > (num_lines-1):
            num_passes += 1
#            print('\n')
#            print(zonename, 'Line 65.  passes =',num_passes, '  num_zones =',num_zones, 'i =', i, '\n')
#            print(iprange, '\n')
            crezones[num_zones] = {'zonename':zonename, 'iprange':iprange}
   
#print(crezones, '\n')

if num_passes == num_zones:
    print('\n')
    i = 1
    for i in crezones:
        print(color.DARKCYAN+crezones[i]['zonename']+color.END)
        print(crezones[i]['iprange'], '\n')

done = False
while not done:
    inp = input(color.PURPLE+'Do you want to create this/these zones in TSC..? (y/n):'+color.END)
    if inp.lower() in ["y", "n"]:
        done = True

if inp == 'y':
    i = 0
    print('\n')
    print(color.RED+'Creating new scan zones on TSC........\n'+color.END)
    for i in crezones:
        sc.scan_zones.create(crezones[i]['zonename'], ips=[crezones[i]['iprange']])
else:
    print('\n')
    print(color.RED+'NOT'+color.END+' creating new scan zones in TSC......\n')

