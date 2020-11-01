#!/usr/bin/env python3
import os
import sys
import time
import socket
import ipaddress
import csv
from operator import itemgetter, attrgetter
from ipaddress import *
from tenable.sc import TenableSC

# define our clear function 

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
Put access key in file called acc.key.  Just the key, one line. Don't press enter. Just save.
Put secret key in a file called sec.key.  Just the key, one line.
The next 2 lines read your access and secret keys so you don't have to expose them in your code.
"""

accesskey = open('adm_acc.key').read().strip()
secretkey = open('adm_sec.key').read().strip()

sc = TenableSC('127.0.0.1', port=8443)
sc.login(access_key = accesskey, secret_key = secretkey)

zonelist = sc.scan_zones.list()

num_zones = len(zonelist)
num_ranges = 0
zoness = {}
tmpzone = {}
srtzone = {}
freerange = {}
newzone = {}
i = 0
p = 1

os.system('clear')

print('\n')
print('Unsorted zone list from API call to TSC.  Number of Scan Zones = ', num_zones,'\n')
print(color.PURPLE+'{:>5} {:<30} {:^70}'.format('ID', 'NAME', 'Zone RANGEs')+color.END)
print(color.PURPLE+'-----------------------------------------------------------------------------------------------------------'+color.END)

for zone in zonelist:
    print('{:>5} {:<30} {:>70}'.format(zone['id'], zone['name'], zone['ipList']))

for zone in zonelist:
    if ',' in str(zone['ipList']):
        for range in zone['ipList'].split(','):
            if ',' in str(zone['ipList']):                
                zoness[i] = {'id':zone['id'], 'name':zone['name'], 'ipList':range}
                i += 1
    else:
        zoness[i] = {'id':zone['id'], 'name':zone['name'], 'ipList':zone['ipList']}
        i += 1

num_ranges = len(zoness)

input()
os.system('clear')

print('\n')
print('Ranges in each scan broken out line by line.  Number of ranges = ', num_ranges, '\n')
print(color.PURPLE+'{:>4} {:<30} {:>32} {:>20} {:>20}'.format('ID', 'NAME', 'RANGE', 'START', 'END')+color.END)
print(color.PURPLE+'--------------------------------------------------------------------------------------------------------------'+color.END)
i = 0
for i in zoness:
    if '-' in str(zoness[i]['ipList']):
        start, end = zoness[i]['ipList'].split('-')
        tmpzone[i] = {'id':zoness[i]['id'], 'name':zoness[i]['name'], 'ipList':zoness[i]['ipList'], 'start':ipaddress.ip_address(start), 'end':ipaddress.ip_address(end)}
        print('{:>4} {:<30} {:>32} {:>20} {:>20}'.format(tmpzone[i]['id'], tmpzone[i]['name'], tmpzone[i]['ipList'], start, end))
    else:
        netrange = zoness[i]['ipList']
        net = ipaddress.ip_network(netrange)
        start = net.network_address
        end = net.broadcast_address
        tmpzone[i] = {'id':zoness[i]['id'], 'name':zoness[i]['name'], 'ipList':zoness[i]['ipList'], 'start':start, 'end':end}
        print('{:>4} {:<30} {:>32} {:>20} {:>20}'.format(tmpzone[i]['id'], tmpzone[i]['name'], tmpzone[i]['ipList'], str(start), str(end)))
    i += 1

tmpzone = sorted(tmpzone.items(), key=lambda item: item[1]['end'])

input()
os.system('clear')

print('\n')
print('Sorted Scan Zone Range List.  Number of Zones = ',num_zones, ' Number of zone ranges = ', num_ranges, '\n')
print(color.PURPLE+'{:>4} {:<30} {:>32} {:>20} {:>20}'.format('ID', 'NAME', 'RANGE', 'START', 'END')+color.END)
print(color.PURPLE+'--------------------------------------------------------------------------------------------------------------'+color.END)
i = 0
for zzone in tmpzone:
    Id = zzone[1]['id']
    name = zzone[1]['name']
    ipList = zzone[1]['ipList']
    start = zzone[1]['start']
    end = zzone[1]['end']
    srtzone[i] = {'id':Id, 'name':name, 'ipList':ipList, 'start':start, 'end':end}
    print('{:>4} {:<30} {:>32} {:>20} {:>20}'.format(Id, name, ipList, str(start), str(end)))
    i = i + 1
print('\n')

num_ranges = len(srtzone)
i = 0
r = 0
passs = 0

input()
os.system('clear')

print('\n')
print(color.PURPLE+'{:>4} {:<30} {:>32} {:>20} {:>20}'.format('ID', 'NAME', 'RANGE', 'START', 'END')+color.END)
print(color.PURPLE+'--------------------------------------------------------------------------------------------------------------'+color.END)

while True:
    if srtzone[0]['start'] == '10.0.0.0':
        ipList = str(srtzone[i]['start'])+'-'+str(srtzone[i]['end'])
        freerange[r] = {'id':srtzone[i]['id'], 'name':srtzone[i]['name'], 'ipList':ipList, 'start':srtzone[i]['start'], 'end':srtzone[i]['end']}
        print('{:>4} {:<30} {:>32} {:>20} {:>20}'.format(freerange[r]['id'], freerange[r]['name'], freerange[r]['ipList'], str(freerange[r]['start']), str(freerange[r]['end'])))
        i += 1
        r += 1
    elif r == 0:
        ipList = '10.0.0.0-'+str(srtzone[i]['start'] - 1)
        freerange[r] = {'id':'--', 'name':'-------', 'ipList':ipList, 'start':'10.0.0.0','end':srtzone[i]['start'] - 1}
        print(color.RED+'{:>4} {:<30} {:>32} {:>20} {:>20}'.format(freerange[r]['id'], freerange[r]['name'], freerange[r]['ipList'], str(freerange[r]['start']), str(freerange[r]['end']))+color.END)
        r += 1
    elif r > 0 and (freerange[r-1]['end'] + 1) == srtzone[i]['start']:
        freerange[r] = {'id':srtzone[i]['id'], 'name':srtzone[i]['name'], 'ipList':srtzone[i]['ipList'], 'start':srtzone[i]['start'],'end':srtzone[i]['end']}
        print('{:>4} {:<30} {:>32} {:>20} {:>20}'.format(freerange[r]['id'], freerange[r]['name'], freerange[r]['ipList'], str(freerange[r]['start']), str(freerange[r]['end'])))
        i += 1
        r += 1
    elif r > 0 and (freerange[r-1]['end'] + 1) != srtzone[i]['start']:
        ipList = (str(freerange[r-1]['end'] + 1))+'-'+(str(srtzone[i]['start'] - 1))
        freerange[r] = {'id':'--', 'name':'-------', 'ipList':ipList, 'start':freerange[r-1]['end'] + 1, 'end':srtzone[i]['start'] - 1}
        print(color.RED+'{:>4} {:<30} {:>32} {:>20} {:>20}'.format(freerange[r]['id'], freerange[r]['name'], freerange[r]['ipList'], str(freerange[r]['start']), str(freerange[r]['end']))+color.END)
        r += 1
    if r > 0:
        if str(freerange[r-1]['end']) == '10.255.255.255':
            break
    if i == num_ranges:
        break
    passs += 1

while True:
    if str(srtzone[i]['start']) == '172.16.0.0':
        ipList = str(srtzone[i]['start'])+'-'+str(srtzone[i]['end'])
        freerange[r] = {'id':srtzone[i]['id'], 'name':srtzone[i]['name'], 'ipList':ipList, 'start':srtzone[i]['start'], 'end':srtzone[i]['end']}
        print('{:>4} {:<30} {:>32} {:>20} {:>20}'.format(freerange[r]['id'], freerange[r]['name'], freerange[r]['ipList'], str(freerange[r]['start']), str(freerange[r]['end'])))
        i += 1
        r += 1
    elif r == 0:
        ipList = '172.16.0.0'+'-'+srtzone[i]['start'] - 1
        freerange[r] = {'id':'--', 'name':'-------', 'ipList':ipList, 'start':'172.16.0.0','end':srtzone[i]['start'] - 1}
        print(color.RED+'{:>4} {:<30} {:>32} {:>20} {:>20}'.format(freerange[r]['id'], freerange[r]['name'], freerange[r]['ipList'], freerange[r]['start'], freerange[r]['end'])+color.END)
        r += 1
    elif r > 0 and (freerange[r-1]['end'] + 1) == srtzone[i]['start']:
        freerange[r] = {'id':srtzone[i]['id'], 'name':srtzone[i]['name'], 'ipList':srtzone[i]['ipList'], 'start':srtzone[i]['start'],'end':srtzone[i]['end']}
        print('{:>4} {:<30} {:>32} {:>20} {:>20}'.format(freerange[r]['id'], freerange[r]['name'], freerange[r]['ipList'], str(freerange[r]['start']), str(freerange[r]['end'])))
        i += 1
        r += 1
    elif r > 0 and (freerange[r-1]['end'] + 1) != srtzone[i]['start']:
        ipList = (str(freerange[r-1]['end'] + 1))+'-'+(str(srtzone[i]['start'] - 1))
        freerange[r] = {'id':'--', 'name':'-------', 'ipList':ipList, 'start':freerange[r-1]['end'] + 1, 'end':srtzone[i]['start'] - 1}
        print(color.RED+'{:>4} {:<30} {:>32} {:>20} {:>20}'.format(freerange[r]['id'], freerange[r]['name'], freerange[r]['ipList'], str(freerange[r]['start']), str(freerange[r]['end']))+color.END)
        r += 1
    if r > 0:
        if str(freerange[r-1]['end']) == '172.31.255.255':
            break
    if i == num_ranges:
        break
    passs += 1

while True:
    if str(srtzone[i]['start']) == '192.168.0.0':
        ipList = str(srtzone[i]['start'])+'-'+str(srtzone[i]['end'])
        freerange[r] = {'id':srtzone[i]['id'], 'name':srtzone[i]['name'], 'ipList':ipList, 'start':srtzone[i]['start'], 'end':srtzone[i]['end']}
        print('{:>4} {:<30} {:>32} {:>20} {:>20}'.format(freerange[r]['id'], freerange[r]['name'], freerange[r]['ipList'], str(freerange[r]['start']), str(freerange[r]['end'])))
        i += 1
        r += 1
    elif r == 0:
        ipList = '192.168.0.0'+'-'+srtzone[i]['start'] - 1
        freerange[r] = {'id':'--', 'name':'-------', 'ipList':ipList, 'start':'192.168.0.0','end':srtzone[i]['start'] - 1}
        print(color.RED+'{:>4} {:<30} {:>32} {:>20} {:>20}'.format(freerange[r]['id'], freerange[r]['name'], freerange[r]['ipList'], str(freerange[r]['start']), str(freerange[r]['end']))+color.END)
        r += 1
    elif r > 0 and (freerange[r-1]['end'] + 1) == srtzone[i]['start']:
        freerange[r] = {'id':srtzone[i]['id'], 'name':srtzone[i]['name'], 'ipList':srtzone[i]['ipList'], 'start':srtzone[i]['start'],'end':srtzone[i]['end']}
        print('{:>4} {:<30} {:>32} {:>20} {:>20}'.format(freerange[r]['id'], freerange[r]['name'], freerange[r]['ipList'], str(freerange[r]['start']), str(freerange[r]['end'])))
        i += 1
        r += 1
    elif r > 0 and (freerange[r-1]['end'] + 1) != srtzone[i]['start']:
        ipList = (str(freerange[r-1]['end'] + 1))+'-'+(str(srtzone[i]['start'] - 1))
        freerange[r] = {'id':'--', 'name':'-------', 'ipList':ipList, 'start':freerange[r-1]['end'] + 1, 'end':srtzone[i]['start'] - 1}
        print(color.RED+'{:>4} {:<30} {:>32} {:>20} {:>20}'.format(freerange[r]['id'], freerange[r]['name'], freerange[r]['ipList'], str(freerange[r]['start']), str(freerange[r]['end']))+color.END)
        r += 1
    if r > 0:
        if str(freerange[r-1]['end']) == '192.168.255.255':
            break
    if i == num_ranges and str(freerange[r-1]['end']) == '192.168.255.255':
        break
    if i == num_ranges:
        break
    passs += 1

if freerange[r-1]['end'] != '192.168.255.255':
    ipList = str((freerange[r-1]['end']) + 1)+'-192.168.255.255'
    freerange[r] = {'id':'--', 'name':'-------', 'ipList':ipList, 'start':freerange[r-1]['end'] + 1, 'end':'192.168.255.255'}
    print('{:>4} {:<30} {:>32} {:>20} {:>20}'.format(freerange[r]['id'], freerange[r]['name'], freerange[r]['ipList'], str(freerange[r]['start']), str(freerange[r]['end'])))

input()
os.system('clear')

print('\n')
i = 0
for i in freerange:
    if freerange[i]['name'] == '-------':
        newzone[i] = {'name':'NewZone', 'ipList':freerange[i]['ipList']}

i = 0
print(color.PURPLE+'{:<30} {:>32}'.format('NAME', 'RANGE')+color.END)
print(color.PURPLE+'---------------------------------------------------------------'+color.END)

for i in newzone:
    print('{:<30} {:>32}'.format(newzone[i]['name'], newzone[i]['ipList']))

input()

print('Writting NewZone ranges to newzones.csv in format for zone create TSC endpoint..............\n')

field_names= ['id', 'name', 'ipList', 'start', 'end']
i = 0
with open('newzone.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['name', 'ipList'])
    for i in newzone:
        writer.writerow(newzone[i])
        i += 1

os.system('ls -l newzone.csv')

print('\n')
