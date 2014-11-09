MatchMeta.Info
==============
MatchMeta.Info uses Python to search a SQLite database for unique full paths from XP, VISTA, WIN2K3, WIN7, WIN2K8, WIN8 and WIN2K12.

Four comparisons are completed to determine if the file name and path traditionally exist on a specific computer.

- Operating Systems - exact full path match 
- Alternate Locations - exact file name match
- Similar Filenames - similar file name comparison
- Potential Options - similar full path comparison

The script or executable must be stored in the same path as the database.

$ ./MatchMeta.Info.py -i "Windows\notepad.exe”

Operating Systems:
* XP
* VISTA
* WIN2K3
* WIN7
* WIN8
 
Alternate Locations:
* windows\system32\dllcache\notepad.exe
* windows\system32\notepad.exe
* windows\syswow64\notepad.exe

Similar Filenames:
* windows\system32\dllcache\notepad.exe
* windows\system32\notepad.exe
* windows\notepad.exe
* windows\system32\dllcache\wnotepad.exe
* windows\syswow64\notepad.exe

Potential Options:
* windows\notepad.exe
