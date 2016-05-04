#!/usr/bin/python

# Parses the .txt output of the checkstyle.jar and overwrites that file with JSON output
# Includes classes that represent Projects, Files, and Errors (or style violations/errors)

import sys
import os
import string
from   subprocess import PIPE,Popen

import json
from json import JSONEncoder

#-----------------------------------------------#
################### CLASSES #####################
#-----------------------------------------------#

# Java Projects
class Project:
	def __init__(self):
		self.name = ""			# project name (/localtmp/java_projects/<name>)
		self.size = 0 			# sum of file sizes
		self.total_errors = 0 	# sum of file error_counts
		self.files = [] 		# list of its versions
		self.file_count = 0 	# num files

	def get_file_f(self,f):
		return files[f]

	def add_file(self,f):
		self.files.append(f)
		self.file_count += 1
		if (f != ""):
			self.total_errors += f.error_count
			self.size += f.size

# .Java Files
class File:
	def __init__(self, p, s):
		self.path = p 			# full path
		self.size = s 			# size in bytes
		self.errors = [] 		# list of errors
		self.error_count = 0	# num errors

	def get_error_e(self,e):
		return errors[e]

	def add_error(self,e):
		self.errors.append(e)
		self.error_count += 1

# Style Errors
class Error:
	def __init__(self,n):
		self.name = n 			# style module type/name

# Little helper encoder class
class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


#-----------------------------------------------#
################## FUNCTIONS ####################
#-----------------------------------------------#

# Parses the output of Checkstyle 
# using the Google Style XML!
def parser(filename):
	# We're gonna make a list of projects
	projects = []
	
	# Create a new project object
	p = Project()

	# Variable which will eventually be a File
	fl = ""

	# Counters
	project_count = 0
	file_count = 0
	error_count = 0

	curr_file_path = ""

	# Iterate through the lines
	with open(filename) as f:
		for line in f:
			line = line.strip()
    		# Check if new project
			if line == "Starting audit...":
				# Create new project and version
				p = Project()
				project_count += 1
				file_count = 0

			# Done with this project
			# So add old file to version
			# Add version to project
			# Add project to list of projects
			if line == "Audit done.":
				# Try getting the path for the project
				try:
					ppath = p.files[0].path.split('/')
					p.name = ppath[7] # for example: "/nv/blue/krj9cr/java/localtmp/java_projects/mDiyo_InfiCraft/inficraft/tweaks/hunger/HTContainer.java"
				except:
					True
				p.add_file(fl)
				projects.append(p)
			
			# Skip any blank lines
			if line == "" :
				continue

			# PARSE LINE
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

				# Check if new file
				if file_location != curr_file_path:
					# Add old file to Version/Project
					if file_count > 0:
						p.add_file(fl)
					
					# Create new file
					curr_file_path = file_location
					
					# Get its size first
					proc = Popen(['du','-sb',curr_file_path], stdout=PIPE)
					out_size = proc.communicate()[0].strip().split()[0]

					# Create the file
					fl = File(curr_file_path, int(out_size))
					file_count += 1
					error_count = 0

				# Split up the rest of this string based on how it's put together
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

				# create an Error and add it to current file
				e = Error(error_type)
				error_count += 1

				fl.add_error(e)

		f.close()

	return projects


#-----------------------------------------------#
############### TIME TO DO STUFF ################
#-----------------------------------------------#

# GET .TXT FILENAME, passed as command line arg
if len(sys.argv) <> 2:
	print "Usage: provide one argument, the input file"
	sys.exit(0)

filename = sys.argv[1]

# Parse the file contents
projects = parser(filename)

# Encode everything as a JSON thing
json_encoding = MyEncoder().encode(projects)
result = json.loads(json_encoding)

# PRINT it pretty and overwrite the same file
with open(filename,'w') as f:
	f.write(json.dumps(result, sort_keys=True, separators=(',', ':')))










