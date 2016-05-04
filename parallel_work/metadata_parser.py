import json

p_num = 0
chunk_num = 1
all_projects = []

def meta_data_parser(file_path):

	global p_num
	global chunk_num
	global all_projects
	chunk_size = 0
	chunk_errors = 0
	projects = []

	with open(file_path) as text_file:
		data = json.load(text_file)

	print "-------------------------------------------------------\n"

	for project in data:
		p_num += 1
		size = project['size']
		errors = project['total_errors']
		name = project['name']
		print "Project " + str(p_num) + ":\t" + str(size) + "\t\t" + str(errors) + "\t\t" + name
		chunk_size += size
		chunk_errors += errors
		projects.append((size, errors, p_num, name))
		all_projects.append((size, errors, p_num, name))
		if p_num % 100 == 0:
			print "\n\tchunk_num:\t" + str(chunk_num) + "\n\tchunk_size:\t" + str(chunk_size) + "\n\tchunk_errors:\t" + str(chunk_errors)
			chunk_num += 1
			chunk_size = 0
			chunk_errors = 0

			projects.sort(key=lambda tup: tup[0])
			i = 0
			while projects[i][0] == 0:
				i += 1
			print "\tSmallest:\t" + str(projects[i][0]) + "\t\t" + str(projects[i][1]) + "\t\t" + str(projects[i][3])
			print "\tMedian:\t\t" + str(projects[(99-i)/2][0]) + "\t\t" + str(projects[(99-i)/2][1]) + "\t\t" + str(projects[(99-i)/2][3])
			print "\tLargest:\t" + str(projects[99][0]) + "\t\t" + str(projects[99][1]) + "\t\t" + str(projects[99][3])
			projects = []
	text_file.close()

def main():
	files = ['1-100', '100-200', '200-300', '300-400', '400-500', '500-600', '600-700', '700-800', '800-900', '900-1000']

	for file in files:
		file_path = '../json/concatted' + file + '_sun.txt'
		meta_data_parser(file_path)
		print "\n"

	all_projects.sort(key=lambda tup: tup[0])
	i = 0
	while all_projects[i][0] == 0:
		i += 1

	d = len(all_projects)
	print "\nMedian:\t\t" + str(all_projects[(d-i)/2][0]) + "\t\t" + str(all_projects[(d-i)/2][1]) + "\t\t" + str(all_projects[(d-i)/2][3])

if __name__ == "__main__": main()