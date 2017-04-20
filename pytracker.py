#!/usr/bin/python
import sqlite3
import hashlib
import os
import sys

if len(sys.argv) != 3:
        print """
Usage
        %s [directory] [extension]
Example
        %s '/home/' '.php'
        """ % (sys.argv[0], sys.argv[0])

        quit();


targetDir = sys.argv[1]
targetExtension = sys.argv[2]
homeDir = os.path.expanduser('~') + '/.pytracker';

if not os.path.isdir(homeDir):
        os.mkdir(homeDir);

def getContentHash(s):
        #print s;
        h = hashlib.md5();
        h.update(s);
        return h.hexdigest();



targetDB = getContentHash(targetDir+'|'+targetExtension)
targetDB = "%s/%s.db" % (homeDir, targetDB)

conn = None
if not os.path.isfile(targetDB):
        conn = sqlite3.connect(targetDB)
        curr = conn.cursor()
        curr.execute("""
        CREATE TABLE files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT NOT NULL,
                on_change TEXT NULL,
                created DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        curr.execute("""
        CREATE TABLE hashes (
                file_id INT(11) NOT NULL,
                hash TEXT NOT NULL,
                created DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """);
else:
        conn = sqlite3.connect(targetDB)



curr = conn.cursor();

for root, subdirs, files in os.walk(targetDir):
        for f in files:
                absFile = os.path.join(root, f)

                if not absFile.endswith(targetExtension):
                        continue;

                with open(absFile , 'rb') as absFileReader:
                        hashed = getContentHash(absFileReader.read())
                        #print "%s - %s" % (absFile, hashed)
                        curr.execute("SELECT f.id, f.path, h.hash, f.on_change FROM files AS f INNER JOIN hashes AS h ON h.file_id = f.id WHERE f.path = ? ORDER BY h.created DESC", ( absFile, ) ) #no need for escape because we know the value structure

                        result = curr.fetchone()
                        #if result is not None:
                        #       print "check hash %s" % result[2]
                        #print result
                        if result is None:
                                #insert in both tables
                                print "New file %s" % absFile
                                curr.execute("INSERT INTO files (path) VALUES ( ? )", ( absFile,  ))
                                curr.execute("INSERT INTO hashes (file_id, hash) VALUES (? , ?)", (curr.lastrowid, hashed, ))
                        elif result[2] != hashed:
                                #hash is not same so its different
                                #insert only in hashed
                                print "File %s is changed" % absFile
                                curr.execute("INSERT INTO hashes (file_id, hash) VALUES (? , ?)", (result[0], hashed, ))
                                #if result[3] is not None:
                                #       os.system(result[3])

conn.commit();
conn.close();

