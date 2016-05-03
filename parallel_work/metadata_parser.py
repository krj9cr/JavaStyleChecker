import json

with open('../json/concatted1-100_sun.txt') as text_file:
	data = json.load(text_file)

p_num = 0
chunk_size = 0
chunk_errors = 0

for project in data:
	p_num += 1
	print "Project " + str(p_num) + ":\t" + str(project['size']) + "\t" + str(project['total_errors'])
	chunk_size += project['size']
	chunk_errors += project['total_errors']
	if p_num % 100 == 0:
		print "\n\tchunk_size:\t" + str(chunk_size) + "\n\tchunk_errors:\t" + str(chunk_errors)
		chunk_size = 0
		chunk_errors = 0