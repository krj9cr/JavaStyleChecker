# JavaStyleChecker
Data Science and Software Engineering - Spring 2016 - Group Project

# JSON Structure:
+ Project
	- idx			(unique id)
	- name 			(e.g. /localtmp/java_projects/<name>)
	- size 			(sum of Files.size)
	- total_errors 	(sum of Files.errors)
	- # files 		(num files in list)
	- Files 		(list of files)
		+ idx			(unique id)
		+ size			(size of file in bytes)
		+ path			(full path to file)
		+ # errors 		(num errors in list)
		+ Errors 		(list of errors)
			- idx 			(unique id)
			- name 			(name/type of style module)

# Research Questions
+ RQ1: ownership vs. errors?
+ RQ2: # commits vs. errors?
+ RQ3: size vs. errors?
+ RQ4: lifespan vs. errors?
+ RQ5: most prominent errors for each style.xml

# Tasks
+ KAREN
	- xredo samples
	- xredo JSON structure
	- xparse projects 0-9
	- parse 1052projects.txt
	- tar em up (only javas and change_logs)
	- move data to Rivanna
	- port to Rivanna

+ KEVIN/SHWETA
	- parse out meaningful information
	- try to answer RQs
	- NoSQL?
