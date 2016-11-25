import subprocess

from search_result import SearchResult


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
