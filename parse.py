#!/usr/bin/python

# This was the orginal Parser that I wrote,
# You provide it with one command line argument, a path to a .gava file

import sys

if len(sys.argv) <> 2:
	print "Usage: provide one argument, the input file"
	sys.exit(0)

filename = sys.argv[1]

with open(filename) as f:
    for line in f:
        if line[0] == "[":
        	#GRAB ALL LINE INFO
        	split = line.partition("[")
        	rest = split[2]
        	split = rest.partition("]")
        	tag = split[0]
        	rest = split[2].lstrip()

        	split = rest.partition(":")
        	file_location = split[0]
        	rest = split[2].lstrip()

        	split = rest.partition(":")
        	line_location = split[0]
        	rest = split[2].lstrip()

        	if (rest[0].isdigit()):
        		split = rest.partition(":")
        		char_location = split[0]
        		rest = split[2].lstrip()
        	else:
        		char_location = -1

        	message = ""
        	rev = rest[::-1]
        	split = rev.partition("[")
        	error_type = split[0][::-1].strip()
        	message = split[2][::-1].strip()

        	if (error_type[-1] == "]"):
        		error_type = error_type[:-1]
        	if (message[-1] == "."):
        		message = message[:-1]

        	print tag, file_location, line_location, char_location, message, error_type, "\n"

        	#DO STUFF WITH LINE INFO
        	