import os

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gio
from utils import files


class SearchResult:
	def __init__(self, file_path):
		full_path = os.path.abspath(file_path)
		self.path = os.path.split(full_path)[0]
		try:
			self.size = files.humansize(os.path.getsize(full_path))
		except:
			self.size = -1
		self.file_name = os.path.split(full_path)[1]

		guessed_content_type = Gio.content_type_guess(filename=full_path, data=None)
		if not guessed_content_type[1]:  # uncertain is false
			self.mimetype = Gio.content_type_get_mime_type(guessed_content_type[0])
		else:
			f = Gio.file_parse_name(file_path)
			f_info = f.query_info('standard::content-type', flags=Gio.FileQueryInfoFlags.NOFOLLOW_SYMLINKS, cancellable=None)
			self.mimetype = f_info.get_content_type()

	def toArray(self):
		return [self.mimetype, self.path, self.file_name, str(self.size)]
