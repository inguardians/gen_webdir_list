#!/usr/bin/env python

###############################################
# Name: gen_webdir_list.py
# Version: 0.1
# Company: InGuardians, Inc.
# Start Date: September 27, 2013
#
# Purpose:
#
#   This script can be used to generate directory and file lists from a specific
#   directory.  The default action is to pull just the directory names and just 
#   the file names and create a separate list of each.  In list mode this script
#   will generate a list of file names with their full path from the root of the
#   specified directory.
#
# NOTE:
#
# Developers: 
#   Cutaway (Don C. Weber)
#
# Resources:
#
# TODO: 
#
# Change Log:
#
############################################

import os,sys
from copy import copy

def find_files(d,flist):
    for e in os.listdir(d):
        tmpdir = d + "/" + e
        if os.path.isfile(tmpdir):
            flist.append(tmpdir[2:])
        if os.path.isdir(tmpdir):
            find_files(tmpdir,flist)

def parse_dir(d,dlist,flist):
    for e in os.listdir(d):
        tmpdir = d + "/" + e
        if os.path.isfile(tmpdir):
            flist.append(e)
        if os.path.isdir(tmpdir):
            dlist.append(e)
            parse_dir(tmpdir,dlist,flist)

def usage():
    print sys.argv[0] + ' [-d] [-q] [-l] [-r <directory>] [-n <name>]'
    print "    -h: This is it."
    print "    -n <name>: name to append to the front of the output filenames"
    print "    -d: Turn on debugging.  Default: off"
    print "    -q: Turn on quiet mode to only write to file and not terminal.  Default: off"
    print "    -r <directory>: Root directory where to start. "
    print "                    Output files always written to starting directory."
    print "    -l: Generate file list only. File list will be full path from current or Root directory."
    sys.exit()

if __name__ == "__main__":

    DEBUG  = False
    QUIET  = False
    list_files = False
    start  = os.path.abspath(os.curdir)
    root   = copy(start)
    dofile = "dirlist.txt"
    fofile = "filelist.txt"
    tab = "    "        # for printing to terminal

    ops = ['-n','-d','-q','-r','-l','-h']
    if len(sys.argv) < 2:
        usage()

    while len(sys.argv) > 1:
        op = sys.argv.pop(1)
        if op == '-h':
            usage()
        if op == '-d':
            DEBUG = True
        if op == '-q':
            QUIET = True
        if op == '-n':
            name = sys.argv.pop(1).rstrip()
            dofile = name + dofile
            fofile = name + fofile
        if op == '-r':
            root = start + "/" + sys.argv.pop(1)
            if not os.path.isdir(root):
                print sys.argv[0] + ": specified root directory is NOT a directory\n"
                usage()
            os.chdir(root)
        if op == '-l':
            list_files = True
        if op not in ops:
            usage()

    dirs  = []
    files = []

    # Parse the directories and return a complete list
    # of directory and file names
    # Use os.curdir to avoid full path names
    if list_files:
        find_files(os.curdir,files)
    else:
        parse_dir(os.curdir,dirs,files)

    # Having issues? Print your control variables
    if DEBUG:
        print "DEBUG:",DEBUG
        print "QUIET:",QUIET
        print "dofile:",dofile
        print "fofile:",fofile
        print "start:",start
        print "root:",root
        print "dirs:",dirs
        print "files:",files

    # Process directories
    if dirs:
        DOF = open(start + "/" + dofile,'w')
        if not QUIET: print "\nListing directories:\n"
        for e in dirs:
            if not QUIET: print tab + e
            DOF.write(e + "\n")
        DOF.close()
    else:
        if DEBUG: print "NO DIRECTORIES LOCATED"

    # Process files
    if files:
        if not QUIET: print "\nListing files:\n"
        FOF = open(start + "/" + fofile,'w')
        for e in files:
            if not QUIET: print tab + e
            FOF.write(e + "\n")
        FOF.close()
    else:
        if DEBUG: print "NO FILES LOCATED"

    # We might have left our original directory
    # Let's return
    os.chdir(start)

