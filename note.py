#!/usr/bin/env python3

import datetime
import os   # Find files/directories
import sys  # Access command arguments
from subprocess import call # Run shell commands internally
import re

text_editor = "vim"
file_arg = ""

def main():
    cur_dir  = os.path.dirname(os.path.realpath(__file__))
    note_dir = "/home/eric/Programs/Python/notes/resources/"

    if   len(sys.argv) == 1:
        print("You didn't supply any arguments!")
    elif len(sys.argv) == 2 :
        if   sys.argv[1] == "push":
            print("This will commit and push the git repo")
            today = datetime.datetime.today()
            call(["git", "add", "."])
            call(["git", "commit", "-m", "Updated notes. {:%Y-%m-%d %H:%M:%S}".format(today)])
            call(["git", "push", "origin", "master"])
        elif sys.argv[1] == "pull":
            print("This will pull the remote repo and overwrite the local notes")
            call(["git", "pull"])
        elif sys.argv[1] == "ls":
            call(["ls", note_dir])
        else:
            # If no command is given, but just
            # a file, then try to edit that file
            f_in = note_dir + sys.argv[1]
            if os.path.isfile(f_in):
                call(["vim", f_in])
            else:
                print("Woah,", sys.argv[1], "doesn't exsist!")
                call(["ls", note_dir])
                y_list = ["y", "yes", "yup", "yea",  "yeah"]
                n_list = ["n", "no", "nope", "nay"]
                response = input().lower()
                if   response in y_list:
                    call(["vim", f_in])
                elif response in n_list:
                    sys.exit()
                else:
                    print("Couldn't parse that, but exiting anyway.")
                    sys.exit()
    else:
        f_in = note_dir + sys.argv[2]
        if   sys.argv[1] == "cat":
            call(["cat", f_in])
        elif sys.argv[1] == "rm":
            call(["rm", f_in])
        elif sys.argv[1] == "ls":
            # Just dump the entirety of the 'ls' command so that
            # the user can specify whatever arguments they want
            ls = sys.argv[1:]
            ls.append(note_dir) # Then specify the notes directory
            call( ls )
        elif sys.argv[1] == "add":
            call(["cp", sys.argv[2], f_in ])
#        else:   # If no command is issued, then edit file
#            f_in = note_dir + sys.argv[2]
#            if os.path.isfile(f_in):
#                call(["vim", f_in])
#            else:
#                print("Woah,", sys.argv[2], "doesn't exsist! Do you want to create it from scratch? \n(Y/n)")
#                call(["ls", note_dir])
#                sys.exit()
#                # y_list = ["y", "yes", "yup", "yea",  "yeah"]
#                # n_list = ["n", "no", "nope", "nay"]
#                # response = input().lower()
#                # if   response in y_list:
#                #     call(["vim", f_in])
#                # elif response in n_list:
#                #     sys.exit()
#                # else:
#                #     print("Couldn't parse that, but exiting anyway.")
#                #     sys.exit()

main()

