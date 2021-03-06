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
				result_list.add_search_result(SearchResult(file_name))
			else:
				print("Found: " + file_name)
			if thread and thread.stopped():
				break
		p.wait()

	if completed_function:
		completed_function()


def simple_search(query, path, thread=None, result_list=None, completed_function=None, ignore_case=True, search_file=True, search_folder=True, search_link=True, max_size=0, min_size=0, owner=None, follow_symlink=False,
                  include_hidden=True):
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

	command = ["find"]

	if follow_symlink:
		command.append("-L")
	else:
		command.append("-P")

	command.append(path)

	if max_size > 0:
		command.append("-size")
		command.append("-" + str(max_size) + "c")
	if min_size > 0:
		command.append("-size")
		command.append("+" + str(min_size) + "c")

	command.append(r'\(')
	for t in search_type_string:
		command.append("-type")
		command.append(t)
		command.append("-or")
	command.pop(len(command) - 1)
	command.append('\)')

	if owner:
		command.append("-user")
		command.append(owner)
	command.append(ignore_case_string)
	command.append('\'' + query + '\'')

	if not include_hidden:
		# it excludes only files and folders starting with a dot but not the content of a folder starting with a . To exclude also the content of an hidden folder: \( ! -regex '\..' \)
		for arg in "\( ! -name '.*' \)".split(" "):
			command.append(arg)

	p = subprocess.Popen(" ".join(command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	if thread:
		thread.set_pid(p.pid)

	print("command executed: " + " ".join(command))

	with p.stdout:
		for line in iter(p.stdout.readline, b''):
			file_name = line.rstrip().decode('utf-8')
			if result_list:
				result_list.add_search_result(SearchResult(file_name))
			else:
				print("Found: " + file_name)
			if thread and thread.stopped():
				break
		p.wait()

	if completed_function:
		completed_function()
