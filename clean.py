#!/usr/bin/python
#-------------------------------------------------------------------------------
#
# clean.py (version 0.1)
# written by ptao
#
# A simple script to remove all the random files left behind by various programs
#
# https://github.com/ptao/clean.py
#
#-------------------------------------------------------------------------------
#
# This program is free software: you can distribute it, modify it, curse its
# very existence, or whatever you want. It's all good.
#
# This program comes without any warranty, written or implied, and I assume no
# responsibility for anything that might occur from its use, including, but not
# limited to: deleting your porn, setting fire to your house, or just generally
# ruining your day.

import argparse
import os
import re
import shutil
import sys

def find_matches(target, dirs, files, symlinks):
    matched_dirs = []
    matched_files = []
    for dirpath, dirnames, filenames in os.walk(target, followlinks=symlinks):
        for dirname in dirnames:
            if dirs.match(dirname):
                matched_dirs.append(os.path.join(dirpath, dirname))
        for filename in filenames:
            if files.match(filename):
                matched_files.append(os.path.join(dirpath, filename))
    return matched_dirs, matched_files

def print_matches(matched_dirs, matched_files):
    for matched_dir in matched_dirs:
        print matched_dir + '/'
    for matched_file in matched_files:
        print matched_file

def remove_matches(matched_dirs, matched_files):
    for matched_dir in matched_dirs:
        shutil.rmtree(matched_dir)
    for matched_file in matched_files:
        os.remove(matched_file)

class Error(Exception):
    def __init__(self, msg):
        self.msg = msg

def main():
    try:
        try:
            mac_dirs = r'\.DS_Store'
            mac_files = r'\._.*'

            windows_files = r'Thumbs.db'

            emacs_files = r'.*~'

            vim_files = r'\..*\.swp|.*~'

            svn_dirs = r'\.svn'

            parser = argparse.ArgumentParser(
                    description="remove crap files and directories\
                    (Default: .DS_Store, ._*, Thumbs.db)")
            parser.add_argument('target',
                    help="directory to be cleaned")
            parser.add_argument('-t', '--test', action='store_true',
                    default=False,
                    help="print files only without deleting")
            parser.add_argument('-s', '--symlinks', action='store_true',
                    default=False,
                    help="follow symlinks (WARNING: could cause infinite loop)")
            parser.add_argument('--mac', action="store_true", default=False,
                    help="match .DS_Store, ._*")
            parser.add_argument('--windows', action="store_true", default=False,
                    help="match Thumbs.db")
            parser.add_argument('--emacs', action="store_true", default=False,
                    help="match .*~")
            parser.add_argument('--vim', action="store_true", default=False,
                    help="match \..*\.swp, .*~")
            parser.add_argument('--svn', action="store_true", default=False,
                    help="match \.svn")
            parser.add_argument('-d', '--dirs', metavar="REGEXP",
                    help="custom pattern for matching directories\
                    (overrides specific flags)")
            parser.add_argument('-f', '--files', metavar="REGEXP",
                    help="custom pattern for matching files\
                    (overrides specific flags)")
            parser.add_argument('-V', '--version', action='version',
                    version='%(prog)s 0.1')
            args = parser.parse_args()

            assert os.path.isdir(args.target), "not a valid directory"

            dirs = ""
            files = ""

            if args.dirs or args.files:
                dirs = args.dirs
                files = args.files
            else:
                if args.mac:
                    dirs += mac_dirs + '|'
                    files += mac_files + '|'
                if args.windows:
                    files += windows_files + '|'
                if args.emacs:
                    files += emacs_files + '|'
                if args.vim:
                    files += vim_files + '|'
                if args.svn:
                    dirs += svn_dirs + '|'
                dirs = dirs.rstrip('|')
                files = files.rstrip('|')
            if not dirs and not files:
                # use default values
                dirs = mac_dirs
                files = mac_files + '|' + windows_files

            # turn patterns into compiles re's
            dirs_re = re.compile(dirs)
            files_re = re.compile(files)

            matched_dirs, matched_files = find_matches(
                    args.target, dirs_re, files_re, args.symlinks)

            print_matches(matched_dirs, matched_files)

            if not args.test:
                remove_matches(matched_dirs, matched_files)

            return 0
        except Exception, msg:
            raise Error(msg)

    except Error, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use -h or --help"
        return 2

if __name__ == '__main__':
    sys.exit(main())
