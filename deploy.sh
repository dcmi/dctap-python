#!/bin/bash 

# This command creates (or refreshes) the website at https://dcmi.github.io/dctap-python/
# The command must be run from the root directory of the https://github.com/dcmi/dctap-python/ repo
# MkDocs must be installed - see http://www.mkdocs.org/#installation
# Behind the scenes, MkDocs will build web pages and use the ghp-import tool to commit them 
# to the gh-pages branch, then push the gh-pages branch to GitHub.

mkdocs gh-deploy
