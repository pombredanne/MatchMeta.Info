#!/usr/bin/python

import re
import os
import sqlite3
import argparse
from simhash import Simhash, SimhashIndex

#########################################################################################################################################

parser = argparse.ArgumentParser()
parser.add_argument('-d','--db', help='MatchMeta.Info SQLite Location',required=True)
parser.add_argument('-f','--flexd', help='F-Response Flexdisk Import',required=True)
parser.add_argument('-n','--near', help='Near Match [ Y | N]',required=True)
parser.add_argument('-o','--os', help='Operating System Types: XP, VISTA, WIN2K3, WIN7, WIN2K8, WIN8, WIN2K12 & WIN10',required=True)
args = parser.parse_args()

#########################################################################################################################################

if(args.near.upper() == 'Y'):
    print '---------------------------------'
    print ' MatchMeta.Info Database Fuzzing'
    print '---------------------------------'

    def get_features(s):
        width = 3
        s = s.lower()
        s = re.sub(r'[^\w]+', '', s)
        return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]

    data = {}
    objs = [(str(k), Simhash(get_features(v))) for k, v in data.items()]
    index = SimhashIndex(objs, k=3)

    if os.path.isfile(args.db):
        print 'MatchMeta.Info Database Located'
        print 'Patience...Loading Index...'
        conn = sqlite3.connect(args.db)
        meta = conn.execute("SELECT path FROM MatchMeta WHERE path NOT LIKE '%winsxs%'")
        count = 1

        for line in meta:
            item = Simhash(get_features(unicode(line[0])))
            count = count+1
            index.add(count,item)

        print index.bucket_size()
        print 'Excluding the WINSXS Directory'
        print '---------------------------------'
        print ' MatchMeta.Info Database Loaded'
        print '---------------------------------'
        conn.close()
    else:
        print 'MatchMeta.Info Database -- FAILED'
        sys.exit()

elif(args.near.upper() == 'N'):
    print 'Skipping MatchMeta.Info Database Fuzzing'
else:
    print 'Please use only Y or N'

#########################################################################################################################################

print 'Building MatchMeta.Info Database Arrays'

pathArray = []
nameArray = []
osArray = []

if os.path.isfile(args.db):
    db = sqlite3.connect(args.db)
    all = db.execute("SELECT path,name FROM MatchMeta")
    
    if args.os == 'XP':
        output = db.execute("SELECT path FROM MatchMeta WHERE XP != '1'")
    elif args.os == 'VISTA':
        output = db.execute("SELECT path FROM MatchMeta WHERE VISTA != '1'")
    elif args.os == 'WIN2K3':
        output = db.execute("SELECT path FROM MatchMeta WHERE WIN2K3 != '1'")
    elif args.os == 'WIN7':
        output = db.execute("SELECT path FROM MatchMeta WHERE WIN7 != '1'")
    elif args.os == 'WIN2K8':
        output = db.execute("SELECT path FROM MatchMeta WHERE WIN2K8 != '1'")
    elif args.os == 'WIN8':
        output = db.execute("SELECT path FROM MatchMeta WHERE WIN8 != '1'")
    elif args.os == 'WIN2K12':
        output = db.execute("SELECT path FROM MatchMeta WHERE WIN2K12 != '1'")
    elif args.os == 'WIN10':
        output = db.execute("SELECT path FROM MatchMeta WHERE WIN10 != '1'")

    for line in output:
        osArray.append(os.path.normpath(os.sep.join(re.split(r'\\|/', line[0]))))

    for line in all:
        pathArray.append(os.path.normpath(os.sep.join(re.split(r'\\|/', line[0]))))
        nameArray.append(os.path.normpath(os.sep.join(re.split(r'\\|/', line[1]))))

else:
    print 'MatchMeta.Info Database -- FAILED'
    sys.exit()

#########################################################################################################################################

if os.path.isfile(args.flexd):
    print 'F-Response Flexdisk CSV Located'
else:
    print 'F-Response Flexdisk CSV Missing -- FAILED'
    sys.exit()

if args.os == 'XP' or args.os == 'VISTA' or args.os == 'WIN2K3' or args.os == 'WIN7' or args.os == 'WIN2K8' or args.os == 'WIN8' or args.os == 'WIN2K12' or args.os == 'WIN10':
    print 'Operating System Supported'
else:
    print 'Unsupported Operating System -- FAILED'
    print 'Options: XP, VISTA, WIN2K3, WIN7, WIN2K8, WIN8, WIN2K12 & WIN10'
    sys.exit()

#########################################################################################################################################

print 'Building F-Response Flexdisk Array'

cpath = []

file = open(args.flexd,'r')
db = sqlite3.connect(args.db)
cursor = db.cursor()

for line in file:
    out = line.split('","')
    try:
        if out[3] == 'alloc' and out[5] == 'file':
            clean = out[1].lower().split(os.sep)
            count = len(clean)
            count = count-1

            try:
                if clean[0] == "users" or clean[0] == "documents and settings":
                    path = out[1].lower().replace(clean[1],"%")
                else:
                    path = out[1].lower()
            except IndexError:
                pass
    
        if clean[0] != '$orphanfiles' and clean[0] != 'system volume information':
            
            cpath.append(os.path.normpath(os.sep.join(re.split(r'\\|/', path))))

    except:
        pass

file.close()

#########################################################################################################################################

print '---------------------------------'
print ' Total F-Response Flexdisk Paths'
print '---------------------------------'
print len(cpath)

match = list(set(cpath) & set(pathArray))

print '---------------------------------'
print ' Total MatchMeta.Info Matches'
print '---------------------------------'
print len(match)

unknown = list(set(cpath) - set(match))

print '---------------------------------'
print ' Total Unknown Paths'
print '---------------------------------'
print len(unknown)

wrongos = list(set(match) & set(osArray))

print '---------------------------------'
print ' Wrong Operating System'
print '---------------------------------'
print len(wrongos)



#########################################################################################################################################

if(args.near.upper() == 'Y'):
    fuzzy = []
    for line in unknown:
        try:
            fuzz = Simhash(get_features(unicode(line)))
            num = index.get_near_dups(fuzz)
            if len(num) != 0:
                fuzzy.append(line)
        except:
            pass

    print '---------------------------------'
    print ' Total Fuzzy Near Matches'
    print '---------------------------------'
    print len(fuzzy)

#########################################################################################################################################

wrongpath = []

for line in unknown:

    clean = line.lower().split(os.sep)
    count = len(clean)
    count = count-1
    wrongpath.append(clean[count])

wpath = list(set(wrongpath) & set(nameArray))

print '---------------------------------'
print ' Wrong Path Location'
print '---------------------------------'
print len(wpath)

#########################################################################################################################################

print '---------------------------------'
print 'Saving Wrong Path Location'

wrong_path = open('wrong_path.txt','w')

for line in unknown:
    clean = line.lower().split(os.sep)
    count = len(clean)
    count = count-1
    try:
        number = wpath.index(clean[count])
    except:
        pass
    if number:
        wrong_path.write(line+"\n")

wrong_path.close()

print 'Saving MatchMeta.Info Matches'

match_path = open('match_path.txt','w')
for line in match:
    match_path.write(line+"\n")
match_path.close()

print 'Saving Unknown Paths'

unknown_path = open('unknown_path.txt','w')
for line in unknown:
    unknown_path.write(line+"\n")
unknown_path.close()

print 'Saving Wrong Operating System'

wrongos_path = open('wrongos_path.txt','w')
for line in wrongos:
    wrongos_path.write(line+"\n")
wrongos_path.close()

if(args.near.upper() == 'Y'):
    print 'Saving Fuzzy Near Matches'
    fuzzy_path = open('fuzzy_path.txt','w')
    for line in fuzzy:
        fuzzy_path.write(line+"\n")
    fuzzy_path.close()

