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
    print ''
    print 'Patience...Loading Index...'
    print ''

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
        conn = sqlite3.connect(args.db)
        meta = conn.execute("SELECT path FROM MatchMeta WHERE path NOT LIKE '%winsxs%'")
        count = 1

        for line in meta:
            item = Simhash(get_features(unicode(line[0])))
            count = count+1
            index.add(count,item)

        print ''
        print index.bucket_size()
        print ''
        print 'Excluding the WINSXS Directory'
        print ''
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

fuzzy = []

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
            
            if(args.near.upper() == 'Y'):
                fuzz = Simhash(get_features(unicode(path)))
                num = index.get_near_dups(fuzz)
                if len(num) > 1:
                    fuzzy.append(path)
    except:
        pass

file.close()

#########################################################################################################################################

if(args.near.upper() == 'Y'):
    fuzzy_file = open('fuzzy_file.txt','w')
    for line in fuzzy:
        fuzzy_file.write(line)
    fuzzy_file.clsoe()







