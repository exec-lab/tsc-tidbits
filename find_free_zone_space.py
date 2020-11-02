#!/usr/bin/env python3

"""
This script was written on an Apple Mac.  It should work on any variant of unix or linux.

This script will NOT run in a windows environment without modification.

This script does NOT analysis public IP ranges.

This script uses netaddr for some of the functions.  Install with 'pip install netaddr'.

*********************************************************************************************
*********                                                                           *********
*********       This tool is NOT an officially supported Tenable project.           *********
*********                                                                           *********
********* Use of this tool is subject to the terms and conditions identified below, *********
********* and is not subject to any license agreement you may have with Tenable.    *********
*********                                                                           *********
*********                                                                           *********
*********  Use of this script is at your own risk.                                  *********
*********                                                                           *********
*********  The author assumes no responsibility for its use or outcomes therein.    *********
*********                                                                           *********
*********                  This code is covered under the                           *********
*********                    GNU GENERAL PUBLIC LICENSE                             *********
*********                     Version 3, 29 June 2007                               *********
*********************************************************************************************
"""

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

"""
The first thing I do is clear the screen, print a statement as to what the following out is and print a heading.
Then I loop through zonelist and print out each scan zone.  All IP ranges in the scan zone are printed out on a single line CSV separated.

We create zone[] dict from zonelist[] that was obtained from a call to the TSC API.
"""

print('\n')
print(color.PURPLE+'{:>5} {:<30} {:^70}'.format('ID', 'NAME', 'Zone RANGEs')+color.END)
print(color.PURPLE+'-----------------------------------------------------------------------------------------------------------'+color.END)

for zone in zonelist:
    print('{:>5} {:<30} {:>70}'.format(zone['id'], zone['name'], zone['ipList']))

print('\n')
print(color.YELLOW+'Non RFC 1918 private IP space will NOT be included in this analysis as it is out of scope.'+color.END)

"""
This next loop looks for a comma in the ipList varable from TSC.  If there is a comma, we then loop over that ipList var for each
of the ranges in that TSC zone and write each range into the dict zoness[].  ELSE... if there is no comma, we'll simply write the ipList
to zoness[].  This is how we break out all of the ranges onto a line each.

In this next loop we create zoness[] dict while we loop through zone[] to split each zone's comma separated ranges into line by line listing.
"""

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

"""
Print each IP range in the scan zones on a separate line.
In the code below and the loop following it, we stop processing waiting for the user to hit enter.  This gives the user time to examine
the scan zones as they entered and extracted from TSC.  Once enter is pressed, we clear the screen, print the header and proceed through the loop.

In the loop below we filter for a - to differentiate the IP ranges that are defined by StartIPaddr - EndIPaddr.  We split the range to determine
the start and end IP address.  If we don't find a - in the range, then we use the ipaddress module to pull out the start and stop IP addresses.
In the case of a range simply being a single IP address, it is then assumed that the netmask is 32 and the start and stop IP addresses are the same.
We print out the zone information in each part of the loop.

Looping over zoness[] dict we create tmpzone[] dict that creates the start and stop IP addresses for all the ranges we've worked with above.
"""

print('\n')
print(color.PURPLE+'Unsorted zone list from API call to TSC.  Number of Scan Zones = ', num_zones, ''+color.END)
input('Hit enter to continue.....')
os.system('clear')

print('\n')
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

"""
The next line is using sorted() to sort the dict tmpzone[].
"""

tmpzone = sorted(tmpzone.items(), key=lambda item: item[1]['end'])

print('\n')
print(color.PURPLE+'Ranges in each scan broken out line by line.  Number of ranges = ', num_ranges, ''+color.END)
input('Hit enter to continue.....')
os.system('clear')

"""
The next loop creates srtzone[] dict that is a sorted list of all scan zone ranges including the start and stop IP addresses.
"""

print('\n')
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

print('\n')
print(color.PURPLE+'Sorted Scan Zone Range List.  Number of Zones = ',num_zones, ' Number of zone ranges = ', num_ranges, ''+color.END)
input('Hit enter to continue.....')
os.system('clear')


"""
The next three while loops loop over the srtzone[] dict to determine if an IP address range is covered by an existing TSC scan zone range or not.
If the range is not within an existing TSC scan zone, it will be written the the dict freerange[] and printed in RED.

While loop one covers the 10.0.0.0/8, loop two covers 172.16.0.0/12 and loop three covers 192.168.0.0/16.
"""

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
    if i == num_ranges and str(freerange[r-1]['end']) == '192.168.255.255':
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


"""
This last if statement covers the top of the 192.168.0.0/16 range.  If this range is within a TSC scan zone, this if won't be executed.  If it is not, this
if statement catches it and writes the last range into freerange[].
"""

if freerange[r-1]['end'] != '192.168.255.255':
    ipList = str((freerange[r-1]['end']) + 1)+'-192.168.255.255'
    freerange[r] = {'id':'--', 'name':'-------', 'ipList':ipList, 'start':freerange[r-1]['end'] + 1, 'end':'192.168.255.255'}
    print('{:>4} {:<30} {:>32} {:>20} {:>20}'.format(freerange[r]['id'], freerange[r]['name'], freerange[r]['ipList'], str(freerange[r]['start']), str(freerange[r]['end'])))


print('\n')
print(color.PURPLE+'All IP ranges with free IP ranges in '+color.RED+'RED'+color.END,'\n')

input('Hit enter to continue.....')
os.system('clear')

"""
This next for loop is to create a dict named newzone[] that is formatted with name and range (called ipList).  There is NO id as newzone[] is used to create
a file newzone.csv and the corresponding TSC API call does use and id.  The id is assigned by TSC upon the scanzone creation.
"""

print('\n')
i = 0
for i in freerange:
    if freerange[i]['name'] == '-------':
        newzone[i] = {'name':'NewZone', 'ipList':freerange[i]['ipList']}

i = 0
print(color.PURPLE+'{:<30} {:>32}'.format('NAME', 'RANGE')+color.END)
print(color.PURPLE+'---------------------------------------------------------------'+color.END)

"""
The next for loop prints out the newzone dict.
"""

for i in newzone:
    print('{:<30} {:>32}'.format(newzone[i]['name'], newzone[i]['ipList']))


"""
The following while loop asks the user if they want to write a newzone.csv file and  then waits for the answer of y or n.  Once we have
input from the user we then filter for y or no.... if y we write the newzone.csv file to the current directory and then perform an ls -l
of the file to show it now exits.  If n we exit.
"""

print('\n')
done = False
while not done:
    inp = input(color.PURPLE+'Would you like to write these free IP ranges to newzones.csv ..?   (y/n):'+color.END)
    if inp.lower() in ["y", "n"]:
        done = True

print('Writting NewZone ranges to newzones.csv in format for zone create TSC endpoint..............\n')

field_names= ['id', 'name', 'ipList', 'start', 'end']
i = 0
with open('newzone.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['name', 'ipList'])
    for i in newzone:
        writer.writerow(newzone[i])
        i += 1

if inp == 'y':

    print('\n')
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
    input('Hit enter to continue.........')
else:
    print('\n')
    print('NOT writing free ranges to newzone.csv.')
    print('\n')
