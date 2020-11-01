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
Put access key in file called acc.key.  Just the key, one line.
Put secret key in a file called sec.key.  Just the key, one line.
The next 2 lines read your access and secret keys so you don't have to expose them in your code.
"""

accesskey = open('adm_acc.key').read().strip()
secretkey = open('adm_sec.key').read().strip()

sc = TenableSC('127.0.0.1', port=8443)
sc.login(access_key = accesskey, secret_key = secretkey)

zones = {}
zoness = {}
delzones = {}
num_lines = 0
num_flds = 0
num_zones = 0
num_passes = 0
izonename = ''
iprange = ''

os.system('clear')
print('\n')

i = 0
for zone in sc.scan_zones.list():
    print(zone['id'], color.DARKCYAN+zone['name']+color.END, zone['ipList'])
    zones[i] = {'id':zone['id'], 'name':zone['name']}
    zoness[i] = {'name':zone['name'], 'ipList':zone['ipList']}
    i += 1

#os.system('clear')
done = False
while not done:
    print('\n')
    inp = input(color.PURPLE+'Would you like to write these zones to curzones.csv ..? (y/n):'+color.END)
    if inp.lower() in ["y", "n"]:
        done = True

if inp == 'y':
    i = 0
    os.system('clear')
    print('\n')
    print(color.PURPLE+'The following scan zone list will be written to'+color.GREEN+' curzones.csv........'+color.PURPLE)
    print('curzones.csv can be used with cre_sczones.py to create these zones on TSC\n'+color.END)
    i = 0
    for zone in zones:
        print(color.DARKCYAN+zoness[i]['name']+color.END, zoness[i]['ipList'])
        i += 1
    print('\n')
    i = 0
    with open('curzones.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['name', 'ipList'])
        for i in zoness:
            writer.writerow(zoness[i])
            i += 1
else:
    print('\n')
    print(color.RED+'NOT'+color.END+' creating curzones.csv  file......\n')

print('Hit enter to continue.....\n')
input()
os.system('clear')
done = False
while not done:
    print('\n')
    inp = input(color.PURPLE+'Would you like to write a delete zone csv file (delzones.csv)..? (y/n):'+color.END)
    if inp.lower() in ["y", "n"]:
        done = True

if inp == 'y':
    print('\n')
    print(color.RED+'The following scan zone list written to delzones.csv........')
    print('delzones.csv can be used with del_sczones.py to delete zones from TSC\n'+color.END,'\n')
    i = 0
    for i in zones:
        print(zones[i]['id'], zones[i]['name'])
        i += 1

    print('\n')
    i = 0
    with open('delzones.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['id', 'name'])

        for i in zones:
#            print(zones[i]['id'], zones[i]['name'])
            writer.writerow(zones[i])
            i += 1
else:
    print('\n')
    print(color.RED+'NOT'+color.END+' creating zones.csv  file......\n')

print('\n')

