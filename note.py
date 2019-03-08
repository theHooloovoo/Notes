#!/usr/bin/env python3

import datetime
import os   # Find files/directories
import sys  # Access command arguments
from subprocess import call # Run shell commands internally
import re

""" Feature list:
      - Edit a file with vim, or print it's contents with 'cat' or 'less'.
      - List the contents of notes/ with either 'ls' or 'tree'.
      - Easily push/pull using git.
"""

def get_files_in_dir(cur_dir):
    files = []
    dirs  = []
    for f in os.listdir(cur_dir):
        if os.path.isfile(f):
            files.append(f)
        else:
            dirs.append(f)
    return [files, dirs]

def ask_yes_no(text):
    """ Returns True/False based on Ye/No input. """
    if text.strip()[0] == 'n' or text.strip()[0] == 'N':
        return False
    else:
        return True

def call_ls(args):
    """ arg should be a list of strings. """
    # Just dump the entirety of the 'ls' command so that
    # the user can specify whatever arguments they want
    call(args)

def call_vim(files, filename):
    """ Invokes vim on 'filename'. If 'filename' cannot be found, then the
        user will be asked if they want to create and edit it.
    """
    call(["vim", filename])
    # if filename in files:
    #     call(["vim", filename])
    # else:
    #     if ask_yes_no(input("File not found. Do you want to make it? [Y/n]: ")):
    #         call(["touch", filename])
    #         call(["vim", filename])

def call_git(arg):
    if   arg == "push":
        call_git_push()
    elif arg == "pull":
        call_git_pull()
    else:
        print("You need to specify wether you are pushing or pulling for git.")

def call_git_push():
    print("This will commit and push the git repo")
    today = datetime.datetime.today()
    call(["git", "add", "."])
    call(["git", "commit", "-m", "Updated notes. {:%Y-%m-%d %H:%M:%S}".format(today)])
    call(["git", "push", "origin", "master"])

def call_git_pull():
    print("This will pull the remote repo and overwrite the local notes")
    call(["git", "pull"])

def main(args):
    files, dirs = get_files_in_dir(".")

    if len(args) == 1:
        print("You need to supply some option for this program.")
        print("  Type 'note help' to see your options.")
    elif args[1] in ["ls", "tree", "cat"]:
        call_ls(args[1:])
    elif args[1] == "cat":
        call_cat(args[1:])
    elif args[1] == "vim" or args[1] == "vi":
        call_vim(files, args[2])
    elif args[1] == "git":
        if len(args) >= 3:
            call_git(args[2])
        else:
            print("'git' command requires invocation of either 'push/pull'.")
    else:
        call_vim(files, args[1])

original_dir = os.getcwd()
home_dir = os.path.expanduser("~")
note_dir = os.path.join(home_dir, "Notes/rsrc/")
print("HOME:", home_dir)
print("NEW_DIR:", note_dir)

os.chdir(note_dir)

main(sys.argv)

os.chdir(original_dir)
