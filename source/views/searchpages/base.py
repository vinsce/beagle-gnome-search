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

		self.search_path = os.path.expanduser("~")
		self.gtk_window = gtk_window
		self.thread = None

		# Button used to open a choose folder dialog
		self.choose_folder_button = Gtk.Button("Path: " + os.path.split(self.search_path)[1])
		self.choose_folder_button.connect("clicked", self.on_folder_clicked)

		self.search_entry = Gtk.SearchEntry()
		self.search_entry.connect("activate", self.execute_search)

		self.search_button = Gtk.Button.new_from_icon_name("system-search-symbolic", Gtk.IconSize.BUTTON)
		self.search_button.connect("clicked", self.execute_search)
		self.cancel_button = Gtk.Button.new_from_icon_name("edit-clear-all-symbolic", Gtk.IconSize.BUTTON)
		self.cancel_button.connect("clicked", self.cancel_search)

		h_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)

		h_box.pack_start(self.choose_folder_button, False, True, 12)
		h_box.pack_start(self.search_entry, True, True, 0)
		h_box.pack_start(self.search_button, False, True, 6)
		h_box.pack_start(self.cancel_button, False, True, 6)

		self.result_list = SearchResultView()

		self.scrolled_window = Gtk.ScrolledWindow()
		self.scrolled_window.set_hexpand(False)
		self.scrolled_window.set_vexpand(True)
		self.scrolled_window.add(self.result_list)
		self.scrolled_window.set_margin_bottom(0)

		self.progress_bar = Gtk.ProgressBar()
		self.progress_bar.pulse()
		self.timeout_id = GObject.timeout_add(50, self.on_timeout, None)

		self.status_bar = Gtk.Statusbar()
		self.context_id = self.status_bar.get_context_id("search_cid")
		self.status_bar.push(self.context_id, "Searching is fun!")
		self.status_bar.set_margin_bottom(0)
		self.status_bar.set_margin_top(0)
		self.status_bar.set_margin_left(0)

		# Adding content to the main layout
		self.pack_start(h_box, False, True, 8)
		self.pack_start(self.scrolled_window, True, True, 0)
		self.pack_start(self.progress_bar, False, True, 0)
		self.pack_start(self.status_bar, False, False, 0)

	def on_timeout(self, user_data):
		self.progress_bar.pulse()
		return True

	def execute_search(self, button):
		self.search_button.hide()
		self.cancel_button.show()
		self.progress_bar.show()

		# Notify to the SearchResultView that the search started
		self.result_list.set_is_searching(True)

		# clears old search result
		self.result_list.clear()

		# creates and starts a new thread
		self.thread = StoppableThread(target=self.effective_search)
		self.thread.start()
		self.status_bar.push(self.context_id, "Search started...")

	def cancel_search(self, button):
		self.thread.stop()

	def effective_search(self):
		default_search(query=self.search_entry.get_text(), path=self.search_path, thread=self.thread, result_list=self.result_list, completed_function=self.search_complete)

	def search_complete(self):
		self.progress_bar.hide()
		self.search_button.show()
		self.cancel_button.hide()

		if self.thread.stopped():
			self.status_bar.push(self.context_id, "Search Canceled")
		else:
			self.status_bar.push(self.context_id, "Search Completed")

		self.result_list.set_is_searching(False)

	def on_folder_clicked(self, widget):
		dialog = Gtk.FileChooserDialog("Choose a folder", self.gtk_window, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))
		dialog.set_default_size(500, 300)

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			self.choose_folder_button.set_label("Path: " + os.path.split(dialog.get_filename())[1])
			self.search_path = dialog.get_filename()

		dialog.destroy()

	def after_show(self):
		self.cancel_button.hide()
		self.progress_bar.hide()
