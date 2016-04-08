#!/usr/bin/python

# A second iteration of stuff
# Includes a bunch of classes that I made up,
# the same parsing function from parse.py,
# and has variable names for the .xml style, .jar executable for checkstyle, and a "Data" folder that contains data

import sys
import os
import string
import subprocess

import paramiko, base64

import json
from json import JSONEncoder

#-----------------------------------------------#
################### CLASSES #####################
#-----------------------------------------------#

# Java Projects
class Project:
	def __init__(self, i):
		self.idx = i
		self.versions = [] # list of its versions
		self.version_count = 0

	def __str__(self):
		v_str = ""
		for v in self.versions:
			v_str += str(v)

		return "{ Project: " + str(self.idx) + "\n" + v_str + "}\n"

	def get_version_v(self,v):
		return versions[v]

	def add_version(self,v):
		self.versions.append(v)
		self.version_count += 1

# Versions of a Project
class Version:
	def __init__(self,i):
		self.idx = i
		self.files = [] # list of files
		self.file_count = 0

	def __str__(self):
		f_str = ""
		for f in self.files:
			f_str += str(f)

		return "  { Version: " + str(self.idx) + "\n" + f_str + "  }\n"

	def get_file_f(self,f):
		return files[f]

	def add_file(self,f):
		self.files.append(f)
		self.file_count += 1

# .Java Files
class File:
	def __init__(self,i,p,n,e):
		self.idx = i
		self.path = p
		self.name = n
		self.errors = e # list of errors
		self.error_count = len(self.errors)

	def __str__(self):
		e_str = ""
		for e in self.errors:
			e_str = e_str + str(e)

		return "    { File: " + str(self.idx) + " " + str(self.name) + "\n" + e_str + "    }\n"

	def get_error_e(self,e):
		return errors[e]

	def add_error(self,e):
		self.errors.append(e)
		self.error_count += 1

# Style Errors
class Error:
	def __init__(self,i,n):
		self.idx = i
		self.name = n

	def __str__(self):
		return "      Error: " + str(self.idx) + " " + str(self.name) + "\n"

# Little helper encoder class
class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


#-----------------------------------------------#
################## FUNCTIONS ####################
#-----------------------------------------------#

# Parses the output of Checkstyle 
# using the Google Style XML!
def parser(str_val):
	# we're gonna make a list of errors
	errors = []
	error_count = 0

	# since we're given a string we need to split it by newline characters
	# so that it becomes lines (but actually an array of strings)
	str_list = string.split(str_val,'\n')

	# iterate through the lines
	for line in str_list:
		# make sure its not a dumb line
		if line == "Audit done." or line == "Starting audit..." or line == "" :
			continue

		# PARSE
		if line[0] == "[":
        	#GRAB ALL STUPID LINE INFO
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

			#errors.append([tag, file_location, line_location, char_location, message, error_type])

			# create an Error and put it in our list
			errors.append(Error(error_count,error_type))
			error_count += 1

	return errors

def SSHconnect():
	# Credentials
	host = "hitchcock.cs.virginia.edu"
	user = "krj9cr"
	pw   = "EILkQL6Q"

	# Create a client
	client = paramiko.SSHClient()
	# Next line gets around the host being "unkown"
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(host, username=user, password=pw)

	return client

def getProjectNames(client):
	# List of all the names
	projects = []

	# Execute ls command 
	stdin, stdout, stderr = client.exec_command('ls /localtmp/java_projects')
	
	# Go through the output
	for line in stdout:
		# Clean up the line and append it
		line = line.strip()
		projects.append(line)

	return projects



#-----------------------------------------------#
############### TIME TO DO STUFF ################
#-----------------------------------------------#

# Path to xml style format
style_path = "google-style.xml"

# Path to checkstyle's .jar file
jar_path = "checkstyle-6.15-all.jar"

# Path to wherever Data is
rootdir = "Data"

# Create a sort of dummy project
p = Project(0)

# And a dummy version
v = Version(0)

# ITERATE through directory's files
for subdir, dirs, files in os.walk(rootdir):
    
    file_count = 0
    
    for file in files:
        # get the full path to the file
        f_path = os.path.join(subdir, file)
        
        # make sure its a java file
        if file.endswith('.java'):
        	# execute shell command and save the output
        	out = subprocess.check_output(['java', '-jar', jar_path, '-c', style_path, f_path])

        	# pass the output to the parser
        	errors = parser(out)

        	# create a file
        	f = File(file_count, f_path, file, errors)

        	# add it to this version
        	v.add_file(f)

# add this version to this project
p.add_version(v)

# encode everything as a JSON thing
json_encoding = MyEncoder().encode(p)
result = json.loads(json_encoding)

# PRINT it pretty
print json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))
'''

# Do stuff with the SSH client
client = SSHconnect()
projects = getProjectNames(client)

# Check out each of the projects
# But actually just one for now
for i in range(0,1):
	# Path to wherever Data is
	rootdir = "/localtmp/java_projects/" + projects[i]

	# Create a sort of dummy project
	p = Project(i)

	# And a dummy version
	v = Version(0)

	# ITERATE through directory's files
	#for subdir, dirs, files in os.walk(rootdir):
	    
	    #file_count = 0
	    
	    #for file in files:
	        # get the full path to the file
	        #f_path = os.path.join(subdir, file)
	        
	        # make sure its a java file
	        #if file.endswith('.java'):
	        	# execute shell command and save the output
	        	#out = subprocess.check_output(['java', '-jar', jar_path, '-c', style_path, f_path])
	out = subprocess.check_output(['java', '-jar', jar_path, '-c', style_path, rootdir])

	print out

	        	# pass the output to the parser
	        	#errors = parser(out)

	        	# create a file
	        	#f = File(file_count, f_path, file, errors)

	        	# add it to this version
	        	#v.add_file(f)

	# add this version to this project
	#p.add_version(v)

# encode everything as a JSON thing
json_encoding = MyEncoder().encode(p)
result = json.loads(json_encoding)

# Close the session
client.close()
'''









