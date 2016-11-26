import os, gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gio
from utils import files


class SearchResult:
	def __init__(self, file_path):
		full_path = os.path.abspath(file_path)
		self.path = os.path.split(full_path)[0]
		try:
			self.size = files.humanize_size(os.path.getsize(full_path))
		except:
			self.size = 0
		self.file_name = os.path.split(full_path)[1]

		guessed_content_type = Gio.content_type_guess(filename=full_path, data=None)
		if not guessed_content_type[1]:  # uncertain is false
			self.mime_type = Gio.content_type_get_mime_type(guessed_content_type[0])
		else:  # uncertain is true, it tries to get the mime type in a second way
			f = Gio.file_parse_name(file_path)
			f_info = f.query_info('standard::content-type', flags=Gio.FileQueryInfoFlags.NOFOLLOW_SYMLINKS, cancellable=None)
			self.mime_type = f_info.get_content_type()

	def to_array(self):
		return [self.mime_type, self.path, self.file_name, str(self.size)]
