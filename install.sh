#!/bin/bash

if [ ! "`whoami`" = "root" ];
then
    echo "Must install as root"
    exit 1
fi;

if [ "`which git`" = "" ];
then
    echo "git is missing"
    exit 1
fi;

if [ "`which python`" = "" ];
then
    echo "python is missing"
    exit 1
fi;

temp_dir=$(mktemp -d)
cd "$temp_dir"

git clone https://github.com/dalibor91/pytracker pytrack

cd pytrack

python setup.py install

rm -rf "$temp_dir"








