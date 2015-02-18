#!/usr/bin/python

import sys, getopt, sqlite3
from fuzzywuzzy import fuzz

def main(argv):
  ItemPath = ''
  try:
    opts, args = getopt.getopt(argv,"hi:",["ItemPath="])
  except getopt.GetoptError:
    print 'MatchMeta.Info.py -i <ItemPath>'
    print '  '
    print '  ItemPath:       \"Windows\System32\services.exe\"'
    print '  '
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'MatchMeta.Info.py -i <ItemPath>'
      print '  '
      print '  ItemPath: \"Windows\System32\services.exe\"'
      print '  '
      sys.exit()
    elif opt in ("-i", "--ItemPath"):
      ItemPath = arg.lower()
   
    MetaInfo = sqlite3.connect('MatchMeta.Info.SQLite')
    cursor = MetaInfo.cursor()
    
    Username = ItemPath.split("\\")
    count = len(Username)
    count = count-1

    try:
      if Username[0] == "users" or Username[0] == "documents and settings":
        ItemPath = ItemPath.replace(Username[1],"%")  
    except IndexError:
      pass

    cursor.execute("SELECT * FROM MetaInfo WHERE ItemPath LIKE:ItemPath", {"ItemPath":ItemPath})
    exists = cursor.fetchone()


    def whichos(exists):  
      if exists[3] == 1:
        print ' ** XP'
      if exists[4] == 1:
        print ' ** VISTA'
      if exists[5] == 1:
        print ' ** WIN2K3'
      if exists[6] == 1:
        print ' ** WIN7'
      if exists[7] == 1:
        print ' ** WIN2K8'
      if exists[8] == 1:
        print ' ** WIN8'
      if exists[9] == 1:
        print ' ** WIN2K12'
      return

    print ' '
    print 'Operating Systems:'
 
    if exists is not None:  
      whichos(exists)

    print ' '

    cursor.execute("SELECT * FROM MetaInfo")
    rows = cursor.fetchall()
    
    arrayAlternateLocation = []
    arraySimpleRatio = []
    arrayPartialRatio = []
    
    for row in rows:
      if Username[count] == row[0] and ItemPath != row[2]:
        arrayAlternateLocation.append(row[2])
      
      PartialRatio = fuzz.partial_ratio(row[2],ItemPath)
      if PartialRatio > 85:
        arrayPartialRatio.append(row[2])
   
      SimpleRatio = fuzz.ratio(row[0],Username[count])
      if SimpleRatio > 85:
        arraySimpleRatio.append(row[2]) 	
 
    print 'Alternate Locations:'

    for l in arrayAlternateLocation:
      print ' ** '+l

    print ' '
    print 'Similar Filenames:'

    for s in arraySimpleRatio:
      print ' ** '+s 

    print ' '
    print 'Potential Options:'

    for p in arrayPartialRatio:
      print ' ** '+p

    cursor.close()
    MetaInfo.close()
    sys.exit()   

if __name__ == "__main__":
  main(sys.argv[1:])
