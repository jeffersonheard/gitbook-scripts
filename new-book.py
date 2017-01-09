#!/usr/bin/python3

# #!/bin/bash
# 
# USER=gregtmobile
# PROTOTYPE=gitbook-prototype
# 
# if [[ $# -eq 0 ]] ; then
#     echo 'Usage: new-book.sh REPOSITORY-NAME'
#     exit 0
# fi
# 
# rm -rf gitbook-prototype.git
# git clone --bare https://github.com/$USER/$PROTOTYPE.git
# cd $PROTOTYPE.git
# git push --mirror git@github.com/$USER/$1.git

import sys
import os
from github import Github
import sh
from sh.contrib import git

######################################################################
# CONFIG VARIABLES. EDIT HERE.

PROTOTYPE_URL = "https://github.com/gregtmobile/gitbook-prototype.git"
PROTOTYPE_NAME = "gitbook-prototype"

######################################################################
# DO NOT EDIT BELOW THIS LINE.

def prompt(s):
   sys.stdout.write(s + ': ')
   sys.stdout.flush()
   return input()

original_working_directory = os.getcwd()
sh.rm('-rf', 'gitbook-prototype.git')

username = prompt('GitHub Username: ')
password = prompt('GitHub Password: ')

print("Logging into GitHub.")
g = Github(username, password)
print("Existing repositories (books) ")
print("-----------------------------\n")
for repo in g.get_user().get_repos():
    print(repo.name)
print("-----------------------------\n\n")

book_name = prompt('Name for New Book: ')

book_library = 'dropbox'
def prompt_booklib():
	global book_library
	book_library = prompt('Location of your GitBook Library (Google Drive or Dropbox)')
	if book_library.lower().startswith('g'):
	   book_library = os.environ['HOME'] + '/Google Drive/GitBooks/books'
	elif book_library.lower().startswith('d'):
	   book_library = os.environ['HOME'] + '/Dropbox/GitBooks/books'
	else:
	   print("Please specify 'Google Drive' or 'Dropbox'")
	   prompt_booklib()
prompt_booklib()

print("Creating new book on GitHub")
new_repo = g.get_user().create_repo(book_name, description=book_name)
print("Created book at " + new_repo.ssh_url)

print("Cloning prototype")
git('clone', '--bare', PROTOTYPE_URL)
os.chdir(PROTOTYPE_NAME + '.git')
sh.git('push', '--mirror', new_repo.ssh_url, _in=sys.stdin, _out=sys.stdout)

print("Removing Temporary Files")
os.chdir(original_working_directory)
sh.rm('-rf', 'gitbook-prototype.git')

print("Adding repo to library")
os.chdir(book_library)
git('clone', new_repo.ssh_url)
os.chdir(new_repo.name)

print("Installing requirements. This may take a minute.")
sh.gitbook('install', _out=sys.stdout)

os.chdir(original_working_directory)



