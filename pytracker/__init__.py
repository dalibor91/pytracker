import os
import uuid

from . import db
from . import str_hash
from . import file as f

home_dir  = os.path.expanduser('~') + '/.pytracker'
run_uuid  = str(uuid.uuid1())
db_exists = False

def help(program):
    return """
Usage
    {program} [directory] [extension] <options>
Options
    --find              [name]      Returns file from db
    --history|-history  [uuid]      Displays history for specific scan or all
    --ignoref|-ignoref  [file]      Ignores file in next scans
    --ignored|-ignored  [dir]       Ignores directory in next scans
    --clear                         Clears database
    --describe          [file_id]   Shows when file was changed
    --help                          Shows this message
    --verbose                       Show aditional messages
""".format(program=program)

def __scan(d, e, db):
    for f_file in f.Finder.find_extension(e, d):
        find_file = db.find_file(f_file.path())
        if find_file is not None:
            #3- ignore file 4 - ignore dir
            if find_file[3] == 1 or find_file[4] == 1:
                continue ;

            #todo

            #check if ignored
            #check if changed
            pass
        else:
            #add file
            pass

def process_args(progra, args):
    if len(args) < 2:
        raise Exception("Directory and extension are missing")

    target_dir = args[0]
    target_ext = args[1]
    storage_db = "%s/%s.db" % (home_dir, str_hash.md5_hash(target_dir + '|' + target_ext))

    if os.path.isfile(storage_db):
        db.initialize(storage_db)
    else:
        db_exists = True

    if len(args) > 2:
        #process aditional arguments
        __process_subargs(storage_db, args[2:])
    else:
        #just scan
        __scan(target_dir, target_ext, storage_db)
