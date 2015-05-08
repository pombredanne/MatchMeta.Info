MatchMeta.Info
==============
MatchMeta.Info uses Python to create and match a SQLite database for unique full paths from XP, VISTA, WIN2K3, WIN7, WIN2K8, WIN8, WIN2K12 and WIN10 obtained from F-Response Flexdisk.

https://www.f-response.com/assets/pdfs/F-ResponseFlexdiskAPIv1-2.pdf

##create_metainfo.py
Inserts the allocated file name and full path into the MatchMeta.Info database in lower case excluding the '$orphanfiles’ and 'system volume information’ folders.  A ‘%’ will replace the username in the path for the ‘users’ and 'documents and settings’ folders.  The operating system is set by placing a ‘1’ in the corresponding column in the database.

###Help Information:
```
./create_metainfo.py -h
usage: create_metainfo.py [-h] -d DB [-f FLEXD] -o OS

optional arguments:
  -h, --help                show this help message and exit
  -d DB, --db DB            MatchMeta.Info SQLite Location
  -f FLEXD, --flexd FLEXD   F-Response Flexdisk Import
  -o OS, --os OS            Operating System Types: 
                              XP
                              VISTA
                              WIN2K3
                              WIN7
                              WIN2K8
                              WIN8
                              WIN2K12
                              WIN10
```
###Example Command:
```
./create_metainfo.py -d MatchMeta.Info -f flexd-csv.csv -o WIN10
```
##match_metainfo.py

##MatchMeta.Info.zip
A sample MatchMeta.Info database compiled from 32 base installs consisting of XP, VISTA, WIN2K3, WIN7, WIN2K8, WIN8 and WIN2K12 machines.
