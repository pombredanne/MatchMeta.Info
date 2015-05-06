#!/usr/bin/python

import os
import sys
import argparse
import sqlite3

parser = argparse.ArgumentParser()
parser.add_argument('-d','--db', help='MatchMeta.Info SQLite Location',required=True)
parser.add_argument('-f','--flexd', help='F-Response Flexdisk Import')
parser.add_argument('-o','--os', help='Operating System Types: XP, VISTA, WIN2K3, WIN7, WIN2K8, WIN8, WIN2K12 & WIN10',required=True)
args = parser.parse_args()


if os.path.isfile(args.db):
    print 'MatchMeta.Info Database Located'
else:
    conn = sqlite3.connect(args.db)
    curr = conn.cursor()
    curr.executescript("""
        CREATE TABLE MatchMeta (
        "name" text COLLATE RTRIM,
        "path" text COLLATE RTRIM,
        "XP" integer,
        "VISTA" integer,
        "WIN2K3" integer,
        "WIN7" integer,
        "WIN2K8" integer,
        "WIN8" integer,
        "WIN2K12" integer,
        "WIN10" integer,
        CONSTRAINT MatchMetaUnique UNIQUE (path COLLATE RTRIM ASC) ON CONFLICT IGNORE
        );
        CREATE INDEX MatchMetaIndex ON MatchMeta ("name" COLLATE RTRIM ASC, "path" COLLATE RTRIM ASC);
        """)
    print 'MatchMeta.Info Database Created'
    conn.commit()
    curr.close()
    conn.close()

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

db = sqlite3.connect(args.db)
cursor = db.cursor()
file = open(args.flexd,'r')

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
            print path
            cursor.execute("INSERT INTO MatchMeta(name,path) VALUES('%s','%s')" % (clean[count], path));
            
            if args.os == 'XP':
                cursor.execute("UPDATE MatchMeta SET XP = '1' WHERE path=:path", {"path":path})
            elif args.os == 'VISTA':
                cursor.execute("UPDATE MatchMeta SET VISTA = '1' WHERE path=:path", {"path":path})
            elif args.os == 'WIN2K3':
                cursor.execute("UPDATE MatchMeta SET WIN2K3 = '1' WHERE path=:path", {"path":path})
            elif args.os == 'WIN7':
                cursor.execute("UPDATE MatchMeta SET WIN7 = '1' WHERE path=:path", {"path":path})
            elif args.os == 'WIN2K8':
                cursor.execute("UPDATE MatchMeta SET WIN2K8 = '1' WHERE path=:path", {"path":path})
            elif args.os == 'WIN8':
                cursor.execute("UPDATE MatchMeta SET WIN8 = '1' WHERE path=:path", {"path":path})
            elif args.os == 'WIN2K12':
                cursor.execute("UPDATE MatchMeta SET WIN2K12 = '1' WHERE path=:path", {"path":path})
            elif args.os == 'WIN10':
                cursor.execute("UPDATE MatchMeta SET WIN10 = '1' WHERE path=:path", {"path":path})
                    
    except:
        pass

file.close()
db.commit()
cursor.close()
db.close()