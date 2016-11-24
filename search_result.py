import os

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gio
from utils import files


class SearchResult():
	def __init__(self, file_path):
		full_path = os.path.abspath(file_path)
		self.path = os.path.split(full_path)[0]
		try:
			self.size = files.humansize(os.path.getsize(full_path))
		except:
			self.size = -1
		self.file_name = os.path.split(full_path)[1]

		self.mimetype = Gio.content_type_get_mime_type(Gio.content_type_guess(filename=full_path, data=None)[0])

	# alternative content_type, val = Gio.content_type_guess('filename=foo.pdf', data=None)

	def toArray(self):
		return [self.mimetype, self.path, self.file_name, str(self.size)]
