#!/usr/bin/python
import sqlite3
import hashlib
import os
import sys
import uuid

program = os.path.basename(sys.argv[0])

if len(sys.argv) < 3:
        print """
Usage
        %s [directory] [extension] [-d]|[-history]|[-history <runid>]
Example
        %s '/home/' '.php'                             - to only check for new files and
        %s '/home/' '.php' -d                          - to track if file is deleted
        %s '/home/' '.php' -history                    - to list history dates with uuid
        %s '/home/' '.php' -history '12345-12345-1234' - to see history for that specific uuid
        """ % (program, program, program, program, program)

        quit();

targetDir = sys.argv[1]
targetExtension = sys.argv[2]
otherArguments = sys.argv[3][1:] if len(sys.argv) > 3 and sys.argv[3].startswith('-')  else ''
homeDir = os.path.expanduser('~') + '/.pytracker';
runuuid = str(uuid.uuid1())

if not os.path.isdir(homeDir):
        os.mkdir(homeDir);

def getContentHash(s):
        h = hashlib.md5();
        h.update(s);
        return h.hexdigest();



targetDB = getContentHash(targetDir+'|'+targetExtension)
targetDB = "%s/%s.db" % (homeDir, targetDB)

conn = None
historyAvailible = True
if not os.path.isfile(targetDB):
        historyAvailible = False
        conn = sqlite3.connect(targetDB)
        curr = conn.cursor()
        curr.execute("""
        CREATE TABLE files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT NOT NULL,
                on_change TEXT NULL,
                on_delete TEXT NULL,
                deleted INTEGER DEFAULT 0,
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
        curr.execute("""
        CREATE TABLE history (
                runid TEXT NOT NULL,
                file_id INTEGER NOT NULL,
                fnew INTEGER DEFAULT 0,
                fchd INTEGER DEFAULT 0,
                fdel INTEGER DEFAULT 0,
                created DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """);
        curr.execute("CREATE INDEX runnid_idx ON history (runid); ")
else:
        conn = sqlite3.connect(targetDB)

curr = conn.cursor();


if otherArguments == 'history':
        if historyAvailible is False:
                print "History is not availible for given arguments"
                quit();
                
        if len(sys.argv) == 4:
                print "%s | %s | %s" % ( "Files No.".ljust(10), "History ID".ljust(40), "Date".ljust(16) )
                for i in curr.execute(" SELECT COUNT(*), h.runid, h.created  FROM history h INNER JOIN files f ON f.id = h.file_id GROUP BY h.runid"):
                        print "%s | %s | %s" % ( str(i[0]).ljust(10), i[1].ljust(40), i[2].ljust(16) )
        elif len(sys.argv) == 5:
                for i in curr.execute(" SELECT f.path, h.fnew, h.fchd, h.fdel, h.created FROM history h INNER JOIN files f ON f.id = h.file_id WHERE h.runid = ? ", (sys.argv[4], )):
                        print "%s %s" % (( 'Modified' if i[2] == 1 else ('New' if i[1] == 1 else 'Deleted' )), i[0])
        quit();

for root, subdirs, files in os.walk(targetDir):
        for f in files:
                absFile = os.path.join(root, f)

                if not absFile.endswith(targetExtension):
                        continue;

                with open(absFile , 'rb') as absFileReader:
                        hashed = getContentHash(absFileReader.read())
                        #print "%s - %s" % (absFile, hashed)
                        curr.execute(
                        """
                        SELECT
                                f.id,
                                f.path,
                                h.hash,
                                f.on_change
                        FROM
                                files AS f
                        INNER JOIN
                                hashes AS h ON
                                        h.file_id = f.id
                        WHERE
                                f.path = ? AND
                                f.deleted = 0
                        ORDER BY h.created DESC

                        """, ( absFile, ) ) #no need for escape because we know the value structure

                        result = curr.fetchone()

                        if result is None:
                                #insert in both tables
                                print "New      %s" % absFile
                                curr.execute("INSERT INTO files (path) VALUES ( ? )", ( absFile,  ))
                                file_id = curr.lastrowid
                                curr.execute("INSERT INTO hashes (file_id, hash) VALUES (? , ?)", (file_id, hashed, ))
                                curr.execute("INSERT INTO history (runid, file_id, fnew) VALUES ( ?, ?, 1)", (runuuid, file_id,))
                        elif result[2] != hashed:
                                #hash is not same so its different
                                #insert only in hashed
                                print "Modified %s " % absFile
                                curr.execute("INSERT INTO hashes (file_id, hash) VALUES (? , ?)", (result[0], hashed, ))
                                curr.execute("INSERT INTO history (runid, file_id, fchd) VALUES ( ?, ?, 1)", (runuuid, result[0],))


if otherArguments.find('d') >= 0:
        ids = []
        for f in curr.execute("SELECT id, path FROM files WHERE deleted = 0"):
                if not os.path.isfile(f[1]):
                        print "Deleted  %s" % f[1]
                        ids.append(f[0])

        for id in ids:
                curr.execute("UPDATE files SET deleted = 1 WHERE id = %d" % id)
                curr.execute("INSERT INTO history (runid, file_id, fdel) VALUES ( ?, ?, 1)", (runuuid, id,))

conn.commit();
conn.close();
