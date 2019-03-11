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

# === Utility Functions ===================================
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

def find_file(path):
    """ Takes in a path-like object (Read the docs for
        os.path), and searches the notes dir recursively for
        the file returning its path.
    """
    return NotImplemented

# === Call External functions =============================
def call_prog(args):
    """ arg should be a list of strings. """
    # Just dump the entirety of the command so that
    # the user can specify whatever arguments they want
    call(args)

def call_vim(files, filename):
    """ Invokes vim on 'filename'. If 'filename' cannot be found, then the
        user will be asked if they want to create and edit it.
    """
    call(["vim", filename])
    # This needs to be able to recursively search the sub-tree.
    # if filename in files:
    #     call(["vim", filename])
    # else:
    #     if ask_yes_no(input("File not found. Do you want to make it? [Y/n]: ")):
    #         call(["touch", filename])
    #         call(["vim", filename])

def call_git(arg):
    """ Invokes the git command to either push or pull the repo. """
    def call_git_push():
        """ Pushes the repo to github. """
        print("This will commit and push the git repo")
        today = datetime.datetime.today()
        call(["git", "add", "."])
        call(["git", "commit", "-m", "Updated notes. {:%Y-%m-%d %H:%M:%S}".format(today)])
        call(["git", "push", "origin", "master"])

    def call_git_pull():
        """ Pulls the repo off from github. """
        print("This will pull the remote repo and overwrite the local notes")
        call(["git", "pull"])

    if   arg == "push":
        call_git_push()
    elif arg == "pull":
        call_git_pull()
    else:
        print("You need to specify wether you are pushing or pulling for git.")

# === Program's Query Functionality =======================
def parse_for_query(query):
    """ Given a search query, determine if there is an
        optional query appended to it.
        If so, then return it, otherwise return empty string.
    """
    index = query.find('@')
    if index == -1:
        return ""
    elif index == len(query)-1:
        # Make sure the final return doesn't index outside the list.
        return ""
    else:
        return query[index+1:]

def find_query(contents, query):
    """ Splits contents into a list of chunkgraphs, then
        returns whichever one starts with the query string.
    """
    for chunk in re.compile("\n\s*\n").split(contents):
        if chunk.startswith(query):
            return chunk
    return ""

# === Main ================================================
def main(args):
    files, dirs = get_files_in_dir(".")
    if len(args) == 1:
        print("You need to supply some option for this program.")
        print("  Type 'note help' to see your options.")
    # Short-cut to edit this file.
    elif args[1] == "self":
        # This gets called when we are inside the notes/rsrc directory.
        call_vim(files, "../note.py")
    # Now Check for specific cammands that may have been issued.
    elif args[1] in ["ls", "tree", "cat"]:
        call_prog(args[1:])
    elif args[1] == "vim" or args[1] == "vi":
        call_vim(files, args[2])
    elif args[1] == "git":
        if len(args) >= 3:
            call_git(args[2])
        else:
            print("'git' command requires invocation of either 'push/pull'.")
    else:
        query = parse_for_query(args[1])
        if query == "":
            call_vim(files, args[1])
        else:
            print("ERR: QUERY IS NOT YET IMPLIMENTED.")

# === Program State =======================================
home_dir = os.path.expanduser("~")
note_dir = os.path.join(home_dir, "Notes/rsrc/")

os.chdir(note_dir)  # Change state of Current Directory.
main(sys.argv)      # Then invoke the main function.

