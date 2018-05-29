# pytrack

Simple program that tracks file changes on your file system.
This is done by remembering md5 hash of files and when next scan is runned
comparing new hash with old one

It was originaly made for monitoring old installation of wordpress, drupal and joomla


Usage
```
Tracking changes on files
Usage
    pytrack [directory] [extension] <options>
Options
    --help  | -help                        Print this message
    --scan  | -scan  [dir] [ext]           Scan directory for extension
    --hist  | -hist  [dir] [ext] [?uuid]   Show history for this directory
    --ignf  | -ignf  [dir] [ext] [file]    Ignore File
    --ignd  | -ignd  [dir] [ext] [dir]     Ignore Directories
    --rmign | -rmign [dir] [ext] [id]      Delete Ignore record

    --files     | -files    [dir] [ext]    Show Files
    --ignores   | -ignores  [dir] [ext]    Print Ignores
    --clear     | -clear    [dir] [ext]    Clear Database

    --verbose   | -verbose                 Print Messages
    --nooutline | -nooutline               Don't print outline

Examples
    pytrack -help
    pytrack -scan  /tmp .php
    pytrack -scan  /tmp .php -verbose
    pytrack -scan  /tmp .php -nooutline
    pytrack -files /tmp .php
    pytrack -ignd  /tmp .php /tmp/cache
```

To set up monitoring for some specific dir
execute
```
pytrack -scan /tmp .php
```

In this case we did setup for /tmp dir and we are monitoring php files
You will get response, something like
```
~ pytrack -scan /tmp .php
NEW      | 30                                   |
CHANGED  | 0                                    |
DELETED  | 0                                    |
RUN_UUID | e6db45ac-6312-11e8-8762-0242ac110003 |
```

NEW - number of new files changed (in our case all files are new because we didn't had setup before)
CHANGED - number of files that changed from last scan
DELETED - number of files that are deleted from last scan
RUN_UUID - Unique ID for specific scan, you can use this to find which files changed or added for current scan

For example if we want to see which files are added in current scan, we run

~ pytrack -hist /tmp .php e6db45ac-6312-11e8-8762-0242ac110003
---------------------------------------------------------------------------------------------
UUID                                 | Path                    | Type | Date                |
---------------------------------------------------------------------------------------------
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-10.php        | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-7.php         | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-4.php         | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-3.php         | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-5.php         | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-1.php         | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-9.php         | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-6.php         | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-8.php         | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-2.php         | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-1/test-10.php | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-1/test-7.php  | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-1/test-4.php  | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-1/test-3.php  | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-1/test-5.php  | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-1/test-1.php  | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-1/test-9.php  | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-1/test-6.php  | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-1/test-8.php  | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-1/test-2.php  | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-2/test-10.php | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-2/test-7.php  | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-2/test-4.php  | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-2/test-3.php  | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-2/test-5.php  | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-2/test-1.php  | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-2/test-9.php  | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-2/test-6.php  | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-2/test-8.php  | NEW  | 2018-05-29 07:35:46 |
e6db45ac-6312-11e8-8762-0242ac110003 | /tmp/test-2/test-2.php  | NEW  | 2018-05-29 07:35:46 |
```

To see all history scans run
```
pytrack -hist /tmp .php
--------------------------------------------------------------------------------------
UUID                                 | New | Changed | Deleted | Date                |
--------------------------------------------------------------------------------------
e6db45ac-6312-11e8-8762-0242ac110003 | 30  | 0       | 0       | 2018-05-29 07:35:46 |
```

You can also use --verbose flag while scanning and it will print out detailed messages with which files are added
which are new, changed or deleted

You can also set up to ignore some directory or file

To ignore specific file run or directory
```
~ #ignore file
~ pytrack -ignf /tmp .php /tmp/test-9.php
~ #ignore dir
~ pytrack -ignd /tmp .php /tmp/test-2
~ #print ignores
~ pytrack -ignores /tmp .php
---------------------------------------------------
ID | Target          | Type | Changed             |
---------------------------------------------------
1  | /tmp/test-9.php | FILE | 2018-05-29 07:42:35 |
2  | /tmp/test-2     | DIR  | 2018-05-29 07:42:46 |
~
~ #remove ignore by id
~ pytrack -rmign /tmp .php 1
~ pytrack -ignores /tmp .php
---------------------------------------------------
ID | Target          | Type | Changed             |
---------------------------------------------------
2  | /tmp/test-2     | DIR  | 2018-05-29 07:42:46 |
```

Use option --nooutline to remove header from output and "-" and "|"

```
~ pytrack -ignores /tmp .php -nooutline
1  /tmp/test-9.php FILE 2018-05-29 07:42:35
```