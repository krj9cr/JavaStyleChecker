#!/usr/bin/python

# This file concatenates together the output of prod-cons.c, which puts files into a folder called jar/

import sys
import os
import string
from   subprocess import PIPE,Popen

# Get filenames from jar/ directory
proc = Popen(['ls','jar/'], stdout=PIPE)
filenames = proc.communicate()[0].strip().split()

# Write to specific file
with open('concatted0-1000_sun.txt', 'w') as outfile:
    # Write a bracket at the beginning to enclose the list of projects
    outfile.write("[")
    # For each file
    for fname in filenames:
        # Open
        with open("jar/"+fname) as infile:
            # For each line, clean it up, and write it out
            for line in infile:
            	line = line.strip()
            	line = line[1:-1]
            	line = " " + line + ","
                
                outfile.write(line)
