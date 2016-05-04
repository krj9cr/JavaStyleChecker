import json

def filename_getter(chunk_num, file_path):

	with open('../json/project_order.txt') as data_file:
		lines = data_file.read().splitlines()
		data_file.close()

	project_names = lines[((chunk_num-1)*100):(chunk_num*100)]
	project_names.sort()

	with open(file_path) as text_file:
		data = json.load(text_file)
		text_file.close()

	chunk_names = []

	for project in data:
	 	if project['name'] in project_names:
	 		project_names.remove(project['name'])
	 	else:
	 		chunk_names.append(project['name'])

	for p in project_names:
		print p

	print "\n------------------------------\n"

	for c in chunk_names:
	 	print c

def main():
	chunk_num = 9
	file_path = '../json/concatted' + '800-900' + '_sun.txt'
	filename_getter(chunk_num, file_path)

if __name__ == "__main__": main()