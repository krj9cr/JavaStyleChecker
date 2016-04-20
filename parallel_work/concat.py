#!/usr/bin/python

import sys
import os
import string
from   subprocess import PIPE,Popen


proc = Popen(['ls','jar/'], stdout=PIPE)
filenames = proc.communicate()[0].strip().split()

start = 0
end = 116

with open('concatted1-100_mediawiki.txt', 'w') as outfile:
    outfile.write("[")
    for fname in filenames:
    	if start < end:
	        with open("jar/"+fname) as infile:
	            for line in infile:
	            	line = line.strip()
	            	line = line[1:-1]
	            	line = " " + line + ","
	                
	                outfile.write(line)
		start += 1
	#outfile.write("]")