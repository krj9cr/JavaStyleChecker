#!/usr/bin/python

# A second iteration of stuff
# Includes a bunch of classes that I made up,
# the same parsing function from parse.py,
# and has variable names for the .xml style, .jar executable for checkstyle, and a "Data" folder that contains data

import sys
import os
import string
from subprocess import PIPE,Popen

import json
from json import JSONEncoder

#-----------------------------------------------#
################### CLASSES #####################
#-----------------------------------------------#

# Java Projects
class Project:
	def __init__(self, i):
		self.idx = i 			# unique id
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
	def __init__(self, i, p, s):
		self.idx = i 			# unique id
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
	def __init__(self,i,n):
		self.idx = i 			# unique id
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
	# we're gonna make a list of errors
	projects = []
	error_count = 0
	
	p = Project(0)

	fl = ""
	project_count = 0
	file_count = 0

	curr_file_path = ""

	# since we're given a string we need to split it by newline characters
	# so that it becomes lines (but actually an array of strings)
	#str_list = string.split(str_val,'\n')

	# iterate through the lines
	with open(filename) as f:
		for line in f:
			line = line.strip()
    		# Check if new project
			if line == "Starting audit...":
				# Create new project and version
				p = Project(project_count)
				project_count += 1
				file_count = 0

			# Done with this project
			# So add old file to version
			# Add version to project
			# Add project to list of projects
			if line == "Audit done.":
				# try getting the path for the project
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
	        	#GRAB ALL STUPID LINE INFO
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

					#out_size = subprocess.check_output(['du','-sb',curr_file_path]).strip().split()[0]
					# Create the file
					fl = File(file_count, curr_file_path, int(out_size))
					file_count += 1
					error_count = 0

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

				# create an Error and add it to current file
				e = Error(error_count,error_type)
				error_count += 1

				fl.add_error(e)

		f.close()

	return projects

'''
import paramiko, base64
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
'''



#-----------------------------------------------#
############### TIME TO DO STUFF ################
#-----------------------------------------------#


# GET .TXT FILENAME, passed as command line arg
if len(sys.argv) <> 2:
	print "Usage: provide one argument, the input file"
	sys.exit(0)

filename = sys.argv[1]


projects = parser(filename)


# encode everything as a JSON thing
json_encoding = MyEncoder().encode(projects)
result = json.loads(json_encoding)

# PRINT it pretty
with open(filename,'w') as f:
	f.write(json.dumps(result, sort_keys=True, separators=(',', ':')))




'''
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









