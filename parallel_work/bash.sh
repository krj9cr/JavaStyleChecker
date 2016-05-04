#!/bin/bash

# Get project name from args
project=$1

# Execute .jar on given project and save to output file
java -jar checkstyle-6.15-all.jar -c sun_checks.xml -o jar/$project.txt localtmp/java_projects/$project

# Parse .jar output and overwrite the same output file
python style.py jar/$project.txt