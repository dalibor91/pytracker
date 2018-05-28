import sqlite3
import os

__instances = {}


def _connection(db):
    if db not in __instances:
        init = os.path.isfile(db)
        __instances[db] = sqlite3.connect(db)

        if not init:
            initialize(db)

    return __instances[db]


def initialize(db_name):
    conn = _connection(db_name)
    curr = conn.cursor()
    curr.execute("""
    CREATE TABLE files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT NOT NULL,
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
    CREATE TABLE ignores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target TEXT NOT NULL,
        is_file INT DEFAULT 1,
        created DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
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
    curr.execute("CREATE INDEX runnid_idx ON history (runid);")
    curr.execute("CREATE UNIQUE INDEX ignore_idx ON ignores (target, is_file)")


def find_file(db_name, file_check):
    curr = _connection(db_name).cursor()
    curr.execute(
    """
        SELECT
            f.id AS id,
            f.path AS path,
            h.hash AS hash,
            CASE i.is_file
              WHEN i.is_file = 1 and i.target = f.path THEN 1 
              ELSE 0
            END ignore_file,
            CASE i.is_file
              WHEN i.is_file = 0 AND f.path LIKE (i.target || '%') THEN 1 
              ELSE 0 
            END ignore_dir
        FROM
            files AS f
        INNER JOIN
            hashes AS h ON h.file_id = f.id 
        LEFT JOIN
            ignores AS i ON f.path LIKE (i.target || '%')
        WHERE f.path = ?
        ORDER BY h.created DESC
    """, (file_check, ))

    return curr.fetchone()


def add_file(db_name, f, h, runid):
    curr = _connection(db_name).cursor()
    curr.execute("INSERT INTO files (path) VALUES ( ? );", (f,))
    curr.execute("INSERT INTO hashes (file_id, hash) VALUES ( last_insert_rowid(), ? );", (h,))
    curr.execute("INSERT INTO history (runid, file_id, fnew) VALUES ( ?, last_insert_rowid(), 1 );", (runid,))
    _connection(db_name).commit()


def add_changed(db_name, file_id, hashed, runid):
    curr = _connection(db_name).cursor()
    curr.execute("INSERT INTO hashes (file_id, hash) VALUES (? , ?)", (file_id, hashed,))
    curr.execute("INSERT INTO history (runid, file_id, fchd) VALUES ( ?, ?, 1)", (runid, file_id,))
    _connection(db_name).commit()


def add_deleted(db_name, file_id, runid):
    curr = _connection(db_name).cursor()
    curr.execute("UPDATE files SET deleted=1 WHERE id = ?", (file_id,))
    curr.execute("INSERT INTO history (runid, file_id, fdel) VALUES ( ?, ?, 1)", (runid, file_id,))
    _connection(db_name).commit()


def add_ignore(db_name, ignore_target, is_file=1):
    _connection(db_name).cursor().execute("INSERT INTO ignores (target, is_file) VALUES (? , ?);", (ignore_target, is_file,))
    _connection(db_name).commit()


def all_ignore(db_name):
    curr = _connection(db_name).cursor()
    curr.execute("SELECT id, target, is_file, created FROM ignores")
    return curr.fetchall()


def remove_ignore(db_name, ignore_target, is_file=1):
    _connection(db_name).cursor().execute("DELETE FROM ignores WHERE target = ? AND is_file = ?;", (ignore_target, is_file,))
    _connection(db_name).commit()


def del_ignore(db_name, id):
    _connection(db_name).cursor().execute("DELETE FROM ignores WHERE id = ?;", (id,))
    _connection(db_name).commit()

def all_files(db_name, deleted=0):
    curr = _connection(db_name).cursor()
    curr.execute("SELECT * FROM files WHERE deleted = ?", (deleted,))
    return curr.fetchall()


def is_ignored(db_name, path):
    curr = _connection(db_name).cursor()
    curr.execute("""
      SELECT 
        * 
      FROM ignores 
      WHERE 
        (target = ? AND is_file=1) OR 
        ( ? LIKE (target || '%') AND is_file = 0)
    """, (path, path,))
    return curr.fetchall()


def all_history(db_name, target=None):
    curr = _connection(db_name).cursor()
    if target is None:
        curr.execute("""
        SELECT 
            h.runid,
            SUM(h.fnew) AS new_files, 
            SUM(h.fchd) AS changed_files, 
            SUM(h.fdel) AS deleted_files, 
            h.created
        FROM history h
        GROUP BY h.runid
        ORDER BY h.created DESC
        """)
    else:
        curr.execute("""
        SELECT 
            h.runid, 
            f.path , 
            h.fnew,
            h.fchd, 
            h.fdel, 
            h.created
        FROM history h 
        INNER JOIN files f ON 
          f.id = h.file_id
        WHERE h.runid = ?
        ORDER BY h.created
        """, (target ,))

    return curr.fetchall()
