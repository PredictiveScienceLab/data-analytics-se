# This script makes and publishes the lecture book
# Author:
# 	Ilias Bilionis
# Date:
# 	5/9/2022

# Make it
jupyter-book build lecturebook --all

# Publish it
ghp-import -n -p -f lecturebook/_build/html