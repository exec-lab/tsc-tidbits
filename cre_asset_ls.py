#!/usr/bin/env python3
import csv
import time
from tenable.sc import TenableSC

"""
Put access key in file called acc.txt.  Just the key, one line.
Put secret key in a file called sec.txt.  Just the key, one line.
The next 2 lines read your access and secret keys so you don't have to expose them in your code.
"""

accesskey = open('acc.key').read().strip()
secretkey = open('sec.key').read().strip()

sc = TenableSC('127.0.0.1', port=8443)
sc.login(access_key = accesskey, secret_key = secretkey)

# Read in CSV file - change name if needed.
f = open('asset_lists.csv')
csv_f = csv.reader(f)

for line in csv_f:
    print('\nAdding ', line[0], 'as ', line[1], 'with IPs', line[3], 'with the tag', line[2])
    # Sleep is necessary or SecurityCenter errors out after about 100 updates
    time.sleep(0.5)
    print ('   Attempting to create asset list in TSC............')
    sc.asset_lists.create(name=line[0], list_type=line[1], description=line[1], tags=line[2], rules=('any', ('ip', 'eq', line[3])))

print('\n')