import os

import gi

from search.find_search import default_search
from utils.threads import StoppableThread
from views.search_result_view import SearchResultView

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GObject


class BaseSearchPage(Gtk.Box):
	def __init__(self, gtk_window=None):
		super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

		self.searchPath = os.path.expanduser("~")
		self.gtk_window = gtk_window

		self.folderButton = Gtk.Button("Path: " + os.path.split(self.searchPath)[1])
		self.folderButton.connect("clicked", self.on_folder_clicked)
		self.entry = Gtk.SearchEntry()
		self.entry.set_text("test*")
		self.entry.connect("activate", self.execute_search)
		self.searchButton = Gtk.Button.new_from_icon_name("system-search-symbolic", Gtk.IconSize.BUTTON)
		self.searchButton.connect("clicked", self.execute_search)

		self.cancelButton = Gtk.Button.new_from_icon_name("edit-clear-all-symbolic", Gtk.IconSize.BUTTON)
		self.cancelButton.connect("clicked", self.cancel_search)

		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)

		hbox.pack_start(self.folderButton, False, True, 12)
		hbox.pack_start(self.entry, True, True, 0)
		hbox.pack_start(self.searchButton, False, True, 6)
		hbox.pack_start(self.cancelButton, False, True, 6)

		self.pack_start(hbox, False, True, 8)

		self.resultList = SearchResultView()

		self.scrolledwindow = Gtk.ScrolledWindow()
		self.scrolledwindow.set_hexpand(False)
		self.scrolledwindow.set_vexpand(True)
		self.scrolledwindow.add(self.resultList)
		self.scrolledwindow.set_margin_bottom(0)
		self.pack_start(self.scrolledwindow, True, True, 0)
		self.progressbar = Gtk.ProgressBar()
		self.pack_start(self.progressbar, False, True, 0)
		self.progressbar.pulse()

		self.timeout_id = GObject.timeout_add(50, self.on_timeout, None)

		self.statusbar = Gtk.Statusbar()
		self.context_id = self.statusbar.get_context_id("search_cid")
		self.statusbar.push(self.context_id, "Searching is fun!")
		self.statusbar.set_margin_bottom(0)
		self.statusbar.set_margin_top(0)
		self.statusbar.set_margin_left(0)
		self.pack_start(self.statusbar, False, False, 0)

	def on_timeout(self, user_data):
		self.progressbar.pulse()
		return True

	def execute_search(self, button):
		self.searchButton.hide()
		self.cancelButton.show()
		self.progressbar.show()

		# clears old search result
		self.resultList.clear()

		# creates and starts a new thread
		self.thread = StoppableThread(target=self.effective_search)
		self.thread.start()
		self.statusbar.push(self.context_id, "Search started...")

	def cancel_search(self, button):
		self.thread.stop()

	def effective_search(self):
		default_search(query=self.entry.get_text(), path=self.searchPath, thread=self.thread, result_list=self.resultList, completed_function=self.search_complete)

	def search_complete(self):
		self.progressbar.hide()

		self.searchButton.show()
		self.cancelButton.hide()

		if self.thread.stopped():
			self.statusbar.push(self.context_id, "Search Canceled")
		else:
			self.statusbar.push(self.context_id, "Search Completed")

	def on_folder_clicked(self, widget):
		dialog = Gtk.FileChooserDialog("Choose a folder", self.gtk_window, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))
		dialog.set_default_size(500, 300)

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			print("Select clicked")
			print("Folder selected: " + dialog.get_filename())
			self.folderButton.set_label("Path: " + os.path.split(dialog.get_filename())[1])
			self.searchPath = dialog.get_filename()
		elif response == Gtk.ResponseType.CANCEL:
			print("Cancel clicked")

		dialog.destroy()

	def after_show(self):
		self.cancelButton.hide()
		self.progressbar.hide()
