### TenableTidBits-TSC

  TenableTidBits for TSC is a collection of useful code bits to perform work on TSC that is sometimes#  difficult to acheive via the GUI.

#  ==> ls_sczones.py

  This code will list all scan zones currently configured on a Tenable.sc (TSC) console.  The code will list the
  the current zones, then ask if you want to write a file called curzones.csv.  This file is a csv list of
  the current scan zones.

#  ==> cre_sczones.py

  This code will read a csv file given as an argument on the command line and then create corresponding
  scan zones on TSC.  The format of the file is give below along with an example:

        zonename,zone ranges
        newzone,10.10.0.0-10.20.255.255

  One IP range per line. You can have multiple lines with the same zone name and the code will concatenate all
  ranges together with the zone name and then create that zone and all ranges on the TSC console.  You can have
  multiple zone names each with multiple IP ranges.... or not.

#  ==> find_free_zone_space.py

  This code will read all current zones on the TSC console and then list them.  This code will not performa any
  analysis on public IP ranges as public IP addresses are expensive already well known.  You then hit enter and the code
  will then list all zones with each IP range on a separate line.  This makes a little easier for one to see the
  ranges more clearly.  Hit enter and the code will sort the IP ranges, one on each line.  Hit enter and the code
  will then parse through the existing IP ranges and identify IP ranges NOT covered by the current scan zones
  on the TSC console.  All IP ranges will be listed on a line by line basis with all uncovered IP ranges printed
  in RED.  The code will then list just the uncovered zone IP ranges and ask if you want write these zones to a file
  called newzone.csv.  This file can then be used with cre_sczones.py to create a zone on TSC that can then be
  assigned a scanner and then regular scan set up to cover this address space.  Moreover, one could set up alerts in TSC#  to trigger when new hosts are discovered in this uncovered IP space.  The code will then list the file that was written
  and post you to hit enter to finish.

#  ==> ls_asset_ls.py

  This code will list all "managed" and "unmanaged" asset lists currently on the TSC console.

#  ==> rm_asset_ls_bytag.py

  This code will take a command line argument as a tag, then loop through all assets in TSC to find those assets that have
  the tag given on the command line.  When it finds that asset list, it will then delete that asset list.  The code will
  print out each asset list it is deleting.  In a future versionm, I'll have it list all target asset lists to be deleted
  and ask the user if they are sure.  This code can be useful for bulk deleting asset lists by simply finding thost asset
  you want to delete and giving them a tag such as "delete".  Then run this as such: 'rm_asset_ls_bytag.py delete'.

#  ==> cre_asset_ls.py

  This code reads the file asset_lists.csv.... this file contains:

       asset list name, asset list type (dyn or static), asset list tag, IP range

  This code is not very advanced and is used to quickly create asset lists in bulk.

  There are a number of additional files needed to run these scripts.

  There are two sets of .key files required.  We need keys from an administrative user in order to do anything with scan zones.
  We also need a secmanager role user keys as well for our asset list code.  The key files are example key files and will not
  work on your system.  You will need to generate your own admin and user keys.

  --> adm_acc.key          This is an admin access key.
  --> adm_sec.key          This is an admin secrete key.
  --> acc.key              Normal user access key.
  --> sec.key              Normal user secrete key.

  --> asset_lists.csv      This is an example asset list csv file.
  

