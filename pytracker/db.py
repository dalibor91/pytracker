import sqlite3

__instances = {};

def _connection(db):
    if db not in __instances:
         __instances[db] = sqlite3.connect(db)
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
            IF( i.is_file = 1 AND i.target = f.path, 1, 0) AS ignore_file,
            IF( i.is_file = 0 AND f.path LIKE (i.target || '%'), 1, 0) AS ignore_dir
        FROM
            files AS f
        INNER JOIN
            hashes AS h ON h.file_id = f.id
        LEFT JOIN
            ignores AS i ON f.path LIKE (i.target || '%')
        WHERE f.path = ? AND f.deleted = 0
        ORDER BY h.created DESC
    """, ( file_check, ) )

    return curr.fetchone()

def add_ignore(db_name, ignore_target, is_file=1):
    _connection(db_name).cursor().execute(
    """
    INSERT INTO ignores (target, is_file) VALUES (? , ?);
    """, (ignore_target, is_file,))

def remove_ignore(db_name, ignore_target, is_file=1):
    _connection(db_name).cursor().execute(
    """
    DELETE FROM ignores WHERE target = ? AND is_file = ?;
    """, (ignore_target, is_file,))

def all_files(db_name, deleted=0):
    curr = _connection(db_name).cursor()
    curr.execute("SELECT * FROM files WHERE deleted = ?", (deleted, ))
