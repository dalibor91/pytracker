import os
import uuid
import datetime

from . import db
from . import str_hash
from . import file as f
from . import args as arg
from . import fmt

home_dir  = os.path.expanduser('~') + '/.pytracker'
run_uuid  = str(uuid.uuid1())
db_exists = False
verbose   = False
os_export = False

if not os.path.isdir(home_dir):
    os.mkdir(home_dir, 700)

def help(program):
    print("""
Tracking changes on files
Usage
    {program} [directory] [extension] <options>
Options
    --help  | -help                        Help Message
    --scan  | -scan  [dir] [ext]           Scan For Extension
    --hist  | -hist  [dir] [ext] [?uuid]   Show History
    --ignf  | -ignf  [dir] [ext] [file]    Ignore File
    --ignd  | -ignd  [dir] [ext] [dir]     Ignore Directory
    --rmign | -rmign [dir] [ext] [id]      Delete Ignore

    --files     | -files    [dir] [ext]    Show Files
    --ignores   | -ignores  [dir] [ext]    Show Ignores
    --clear     | -clear    [dir] [ext]    Clear Database

    --verbose   | -verbose                 Print Messages
    --nooutline | -nooutline               Don't print outline
    --env_export| -env_export              Print variables

Variables if 'env_export' is enabled:
    $PYTRACK_NEW $PYTRACK_CHANGED $PYTRACK_UUID $PYTRACK_DELETED

Examples
    {program} -help
    {program} -scan  /tmp .php
    {program} -scan  /tmp .php -verbose
    {program} -scan  /tmp .php -nooutline
    {program} -files /tmp .php
    {program} -ignd  /tmp .php /tmp/cache
""".format(program=program))


def __log(msg):
    if verbose:
        print("[ %s ] %s" % (str(datetime.datetime.now()), str(msg)))


def __check__(dir, ext):
    if dir is None or (not os.path.isdir(dir)):
        raise Exception("Dir '%s' does not exists " % str(dir))

    if ext is None:
        raise Exception("Extension can not be None")


def __add_ignore(_db, target, is_file):
    if target is None:
        raise Exception("Ignore target is None")

    db.add_ignore(_db, target, is_file)


def __del_ignore(_db, id):
    if id is None:
        raise Exception("Ignore ID is None")

    db.del_ignore(_db, id)


def __find_ignore(_db):
    _data = db.all_ignore(_db)
    _new_data = []

    for _row in _data:
        _new_data.append((_row[0], _row[1], "FILE" if _row[2] == 1 else "DIR", _row[3]))

    return fmt.print_formated(_new_data, ("ID", "Target", "Type", "Changed"))


def __clear_db(_db):
    if os.path.isfile(_db):
        os.unlink(_db)


def __find_hist(_db, target):
    if target is None :
        return fmt.print_formated(db.all_history(_db), ("UUID", "New", "Changed", "Deleted", "Date"))

    _data = db.all_history(_db, target)
    _filtered = []
    for r in _data:
        _type = "UNKNOWN"
        if r[2] == 1:
            _type = "NEW"
        elif r[3] == 1:
            _type = "CHANGED"
        elif r[4] == 1:
            _type = "DELETED"

        _filtered.append((r[0], r[1], _type, r[5],))
    return fmt.print_formated(_filtered, ("UUID", "Path", "Type", "Date"))


def __scan(d, e, _db):
    data = {
        "new": 0,
        "changed" : 0,
        "deleted" : 0,
        "uuid" : run_uuid
    }
    for f_file in f.Finder.find_extension(e, d):
        find_file = db.find_file(_db, f_file.path())
        if find_file is None:
            _is_ignore = db.is_ignored(_db, f_file.path())
            if _is_ignore is None or len(_is_ignore) == 0:
                __log("ADD     %s" % f_file.path())
                data["new"] += 1
                db.add_file(_db, f_file.path(), f_file.md5_hash(), run_uuid)
            else:
                __log("IGNORE  %s" % f_file.path())
        else:
            if find_file[3] == 1 or find_file[4] == 1:
                __log("IGNORE  %s" % f_file.path())
                continue

            new_hash = f_file.md5_hash()
            if find_file[2] != new_hash:
                data["changed"] += 1
                __log("CHANGED %s" % f_file.path())
                db.add_changed(_db, find_file[0], new_hash, run_uuid)

    for fl in db.all_files(_db):
        if not os.path.isfile(fl[1]):
            data["deleted"] += 1
            __log("DELETED %s" % fl[1])
            db.add_deleted(_db, fl[0], run_uuid)

    #export variables
    if os_export:
        for _dk, _dv in data.items():
            if _dk == 'uuid':
                print("export %s=\"%s\""%(("PYTRACK_%s"%(_dk.upper())), str(_dv)))
            else:
                print("export %s=%s"%(("PYTRACK_%s"%(_dk.upper())), str(_dv)))
        return None

    return fmt.print_formated([ ("NEW", data["new"]), ("CHANGED", data["changed"]), ("DELETED", data["deleted"]), ("RUN_UUID", data["uuid"]) ])


def __show_files(_db):
    return fmt.print_formated(db.all_files(_db), ("ID", "Path", "Deleted", "Created"))



def process_args(program, args):
    global verbose
    global os_export

    args = arg.Arguments(args)

    if args.has("help"):
        return help(program)

    if args.has("verbose"):
        verbose = True

    if args.has("nooutline"):
        fmt.print_outlinte = False

    if args.has("env_export"):
        os_export = True

    if args.has("scan"):
        dir, ext = args.get("scan", 2)
        __check__(dir, ext)
        return __scan(dir, ext, ("%s/%s.db" % (home_dir, str_hash.md5_hash((dir + '|' + ext).encode('utf-8')))))

    if args.has("ignf"):
        dir, ext, target = args.get("ignf", 3)
        __check__(dir, ext)
        return __add_ignore(("%s/%s.db" % (home_dir, str_hash.md5_hash((dir + '|' + ext).encode('utf-8')))), target, 1)

    if args.has("ignd"):
        dir, ext, target = args.get("ignd", 3)
        __check__(dir, ext)
        return __add_ignore(("%s/%s.db" % (home_dir, str_hash.md5_hash((dir + '|' + ext).encode('utf-8')))), target, 0)

    if args.has("hist"):
        dir, ext, target = args.get("hist", 3)
        __check__(dir, ext)
        return __find_hist(("%s/%s.db" % (home_dir, str_hash.md5_hash((dir + '|' + ext).encode('utf-8')))), target)

    if args.has("ignores"):
        dir, ext = args.get("ignores", 2)
        __check__(dir, ext)
        return __find_ignore(("%s/%s.db" % (home_dir, str_hash.md5_hash((dir + '|' + ext).encode('utf-8')))))

    if args.has("files"):
        dir, ext = args.get("files", 2)
        __check__(dir, ext)
        return __show_files(("%s/%s.db" % (home_dir, str_hash.md5_hash((dir + '|' + ext).encode('utf-8')))))

    if args.has("clear"):
        dir, ext = args.get("clear", 2)
        __check__(dir, ext)
        return __clear_db(("%s/%s.db" % (home_dir, str_hash.md5_hash((dir + '|' + ext).encode('utf-8')))))

    if args.has("rmign"):
        dir, ext, id = args.get("rmign", 3)
        __check__(dir, ext)
        return __del_ignore(("%s/%s.db" % (home_dir, str_hash.md5_hash((dir + '|' + ext).encode('utf-8')))), id)

    return help(program)