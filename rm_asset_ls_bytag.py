#!/usr/bin/env python3
import sys
import time
from tenable.sc import TenableSC

"""
This class allows you to redirect error out from standard out to say... /dev/null.
You have to import sys... create the class then call sys.stderr = DevNull() in your code.  Now, errors won't
print to your standard out.... this is useful if you're using the try method and want only your print statement
to output to the shell and not your print and the system error.
"""
class DevNull:
    def write(self, msg):
        pass

"""
The tag you want to delete is the first argument on the command line.  For example: rm_dyn_ls.py acme
"""
tagg = sys.argv[1]

"""
Put access key in file called acc.key.  Just the key, one line. Don't press enter.  Just save.
Put secret key in a file called sec.key.  Just the key, one line.
The next 2 lines read your access and secret keys so you don't have to expose them in your code.
"""

accesskey = open('acc.key').read().strip()
secretkey = open('sec.key').read().strip()

sc = TenableSC('127.0.0.1', port=8443)
sc.login(access_key = accesskey, secret_key = secretkey)

"""
Read manageable asset lists into sclist then obtain the length of the list and assign it to total.  total will be the range 
    for our inner loop.  We use i to count and compare to total so we know when to break out of the loop.
    We loop through sclist to obtain the asset list id, then use the id in the call to sc.asset_lists.details() to get that list's
    tag.  tag is not in sc.asset_lists so we have to make the call to the .details method.
    Once we have identified an asset list with the target tag, we call the .delete() method and pass it the id.
You can also us the usable asset lists as well.... but it seems that manageable asset lists are a super set.
    manageable = read write
    usable = read only
"""
i = 0

"""
I make two calls to TSC below.  This first call, sclist = sc.asset_lists.list() puts all asset lists into sclist.  Next, in the loops
below I loop through sclist to pull out the id of each asset list.  I then use the id in a call to sc.asset_lists.details to pull the asset list tag.
I have to do it this way due to the fact that calling sc.asset_lists.details() only gives you the data for ONE asset list while sc.asset_list.list() 
gives you all of the lists.

I then compare the asset list's tag to the tag entered on the command to determine if I should delete it or not.  The delete is accomplished with
the call sc.asset_lists.delete() where I give it the id.  Continue the loop until I reach the end.
"""

sclist = sc.asset_lists.list()
total = len(sclist['manageable'])

for element in sclist:
    for value in sclist['manageable']:
        if i >= total:
            break
        asset = sc.asset_lists.details(sclist['manageable'][i]['id'])
        if asset['tags'] == tagg:
            print('Deleting Asset List.........')
            print ('{0:>6} {1:>4} {2:>6} {3:<67} {4:<6} {5:>7} {6:>5} {7:<8} {8:<7} {9:<10} {10:^1} {11:<15}'.format('ID =', asset['id'],
                'NAME =', asset['name'],'TYPE =', asset['type'], 'TAG =', asset['tags'], 'OWNER =', asset['owner']['firstname'],
                ' ',asset['owner']['lastname']))
            print('\n')
            time.sleep(2)
            sc.asset_lists.delete(asset['id'])
        i = i + 1
print('\n')


