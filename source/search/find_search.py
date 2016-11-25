import subprocess

from search.search_result import SearchResult


def default_search(query, path, thread=None, result_list=None, completed_function=None):
	p = subprocess.Popen(["find", path, "-iname", query], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	if thread:
		thread.set_pid(p.pid)

	with p.stdout:
		for line in iter(p.stdout.readline, b''):
			file_name = line.rstrip().decode('utf-8')
			if result_list:
				result_list.addItem(SearchResult(file_name))
			else:
				print("Found: " + file_name)
			if thread and thread.stopped():
				break
		p.wait()

	if completed_function:
		completed_function()


def simple_search(query, path, thread=None, result_list=None, completed_function=None, ignore_case=True, search_file=True, search_folder=True, search_link=True, max_size=""):
	if ignore_case:
		ignore_case_string = "-iname"
	else:
		ignore_case_string = "-name"
	search_type_string = ""
	if search_file:
		search_type_string += "f"
	if search_folder:
		search_type_string += "d"
	if search_link:
		search_type_string += "l"

	command = ["find", path]

	if max_size != "":
		ok = True
		try:
			numeric_value = int(max_size[:-1])
		except:
			print("Invalid size")
			numeric_value = 0
			ok = False
		unit_value = max_size[-1:]
		if unit_value == "G":
			byte_value = numeric_value * 1073741824
		elif unit_value == "M":
			byte_value = numeric_value * 1048576
		elif unit_value == "k":
			byte_value = numeric_value * 1024
		elif unit_value == "c":
			byte_value = numeric_value
		elif unit_value == "b":
			byte_value = numeric_value * 512
		else:
			ok = False

		if ok:
			command.append("-size")
			command.append("-" + str(byte_value) + "c")

	command.append(r'\(')
	for t in search_type_string:
		command.append("-type")
		command.append(t)
		command.append("-or")
	command.pop(len(command) - 1)
	command.append('\)')
	command.append(ignore_case_string)
	command.append('\'' + query + '\'')
	p = subprocess.Popen(" ".join(command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	if thread:
		thread.set_pid(p.pid)

	# with p.stderr:
	#	for line in iter(p.stderr.readline, b''):
	#		print("err: " + str(line))
	#	p.wait()
	with p.stdout:
		for line in iter(p.stdout.readline, b''):
			file_name = line.rstrip().decode('utf-8')
			if result_list:
				result_list.addItem(SearchResult(file_name))
			else:
				print("Found: " + file_name)
			if thread and thread.stopped():
				break
		p.wait()

	if completed_function:
		completed_function()
