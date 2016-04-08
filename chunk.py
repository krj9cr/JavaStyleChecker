#!/usr/bin/python

# Runs chunks of projects and gets the output

import sys
import os
import string
import subprocess

project_names = subprocess.check_output(["ls", "/localtmp/java_projects/"])

print project_names

'''
# Path to xml style format
style_path = "google-style.xml"

# Path to checkstyle's .jar file
jar_path = "checkstyle-6.15-all.jar"

for i in range(0,10):
	f_path = "/localtmp/java_projects/" + project_names[i]
	out_path = "project" + str(i) + ".txt"

	print f_path
	
	subprocess.call(['time','java', '-jar', jar_path, '-c', style_path, f_path, '>', out_path])
'''