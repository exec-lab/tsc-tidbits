#!/usr/bin/env python3
import sys
import time
import pprint
from tenable.sc import TenableSC

class DevNull:
    def write(self, msg):
        pass

"""
Put access key in file called acc.key.  Just the key, one line. Don't press enter.  Just save.
Put secret key in a file called sec.key.  Just the key, one line.
The next 2 lines read your access and secret keys so you don't have to expose them in your code.
"""

accesskey = open('acc.key').read().strip()
secretkey = open('sec.key').read().strip()

sc = TenableSC('127.0.0.1', port=8443)
sc.login(access_key = accesskey, secret_key = secretkey)

sclist = sc.asset_lists.list()
i = int
i = 0
total = len(sclist['usable'])
print ('\nTotal usable asset lists = ',len(sclist['usable']))
print('\n')
for element in sclist:
    for value in sclist['usable']:
        if i >= total:
            break
        asset = sc.asset_lists.details(sclist['usable'][i]['id'])
        print ('{0:<4} {1:>3} {2:>6} {3:<67} {4:<6} {5:>7} {6:>5} {7:<8} {8:<7} {9:<10} {10:^1} {11:<15}'.format('ID =', asset['id'],
            'NAME =', asset['name'],'TYPE =', asset['type'], 'TAG =', asset['tags'], 'OWNER =', asset['owner']['firstname'],
            ' ',asset['owner']['lastname']))
        i = i + 1
print('\n')

i = 0
total = len(sclist['manageable'])
print ('\nTotal manageable asset lists = ',len(sclist['manageable']))
print('\n')
for element in sclist:
    for value in sclist['manageable']:
        if i >= total:
            break
        asset = sc.asset_lists.details(sclist['manageable'][i]['id'])
        print ('{0:<4} {1:>3} {2:>6} {3:<67} {4:<6} {5:>7} {6:>5} {7:<8} {8:<7} {9:<10} {10:^1} {11:<15}'.format('ID =', asset['id'],
            'NAME =', asset['name'],'TYPE =', asset['type'], 'TAG =', asset['tags'], 'OWNER =', asset['owner']['firstname'],
            ' ',asset['owner']['lastname']))
        i = i + 1
print('\n')

