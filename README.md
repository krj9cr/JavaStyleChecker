# JavaStyleChecker
Data Science and Software Engineering - Spring 2016 - Group Project

# JSON Structure:
+ Project
	- name 			(e.g. /localtmp/java_projects/<name>)
	- size 			(sum of Files.size)
	- total_errors 	(sum of Files.errors)
	- # files 		(num files in list)
	- Files 		(list of files)
		+ size			(size of file in bytes)
		+ path			(full path to file)
		+ # errors 		(num errors in list)
		+ Errors 		(list of errors)
			- name 			(name/type of style module)

# Research Questions
+ RQ1: ownership vs. errors?
+ RQ2: # commits vs. errors?
+ RQ3: size vs. errors?
+ RQ4: lifespan vs. errors?
+ RQ5: most prominent errors for each style.xml

