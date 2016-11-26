import os

import gi

from search.find_search import simple_search
from utils.threads import StoppableThread
from views.file_size_units_view import FileSizeUnitsView
from views.search_result_view import SearchResultView

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GObject


class SimpleSearchPage(Gtk.Box):
	def __init__(self, gtk_window=None):
		super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

		self.searchPath = os.path.expanduser("~")
		self.searchFile = True
		self.searchDirectory = True
		self.searchLink = True
		self.ignoreCase = True

		self.gtk_window = gtk_window

		self.right_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)

		self.folder_button = Gtk.Button("Path: " + os.path.split(self.searchPath)[1])
		self.folder_button.connect("clicked", self.on_folder_clicked)
		self.entry = Gtk.SearchEntry()
		self.entry.connect("activate", self.execute_search)
		self.search_button = Gtk.Button.new_from_icon_name("system-search-symbolic", Gtk.IconSize.BUTTON)
		self.search_button.connect("clicked", self.execute_search)
		self.cancel_button = Gtk.Button.new_from_icon_name("edit-clear-all-symbolic", Gtk.IconSize.BUTTON)
		self.cancel_button.connect("clicked", self.cancel_search)

		h_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)

		h_box.pack_start(self.folder_button, False, True, 12)
		h_box.pack_start(self.entry, True, True, 0)
		h_box.pack_start(self.search_button, False, True, 6)
		h_box.pack_start(self.cancel_button, False, True, 6)

		# Left panel: search parameters
		self.left_panel = Gtk.ListBox()
		self.left_panel.set_selection_mode(Gtk.SelectionMode.NONE)

		# Ignore case switch
		row = Gtk.ListBoxRow()
		row_alignment = Gtk.Alignment()
		row_alignment.set_padding(8, 8, 4, 4)
		row_alignment.add(row)
		ignore_case_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
		row.add(ignore_case_box)
		ignore_case_label = Gtk.Label(xalign=0)
		ignore_case_label.set_text("Ignore case")
		self.ignore_case_switch = Gtk.Switch()
		self.ignore_case_switch.connect("notify::active", self.on_ignore_case_changed)
		self.ignore_case_switch.set_active(True)
		ignore_case_box.pack_start(ignore_case_label, True, True, 0)
		ignore_case_box.pack_end(self.ignore_case_switch, False, True, 0)
		self.left_panel.add(row_alignment)

		# File Type checkboxes
		row = Gtk.ListBoxRow()
		row_alignment = Gtk.Alignment()
		row_alignment.set_padding(8, 8, 4, 4)
		row_alignment.add(row)
		file_types_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
		row.add(file_types_box)
		file_types_label = Gtk.Label(xalign=0)
		file_types_label.set_text("Types")
		self.file_type_file_button = Gtk.CheckButton.new_with_label("File")
		self.file_type_file_button.connect("toggled", self.on_button_toggled, "file")
		self.file_type_file_button.set_active(True)
		self.file_type_folder_button = Gtk.CheckButton.new_with_label("Folder")
		self.file_type_folder_button.set_active(True)
		self.file_type_folder_button.connect("toggled", self.on_button_toggled, "folder")
		self.file_type_link_button = Gtk.CheckButton.new_with_label("Link")
		self.file_type_link_button.set_active(True)
		self.file_type_link_button.connect("toggled", self.on_button_toggled, "link")

		file_types_box.pack_start(file_types_label, True, True, 0)
		checkboxes_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
		checkboxes_box.pack_start(self.file_type_file_button, True, False, 0)
		checkboxes_box.pack_start(self.file_type_folder_button, False, False, 0)
		checkboxes_box.pack_start(self.file_type_link_button, False, False, 0)
		file_types_box.pack_end(checkboxes_box, False, True, 0)
		self.left_panel.add(row_alignment)

		# Max size
		row = Gtk.ListBoxRow()
		row_alignment = Gtk.Alignment()
		row_alignment.set_padding(8, 8, 4, 4)
		row_alignment.add(row)
		max_size_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=48)
		row.add(max_size_box)
		max_size_label = Gtk.Label(xalign=0)
		max_size_label.set_text("Max size")
		self.max_size_view = FileSizeUnitsView()
		max_size_box.pack_start(max_size_label, True, True, 0)
		max_size_box.pack_end(self.max_size_view, False, True, 0)
		self.left_panel.add(row_alignment)

		# Min size
		row = Gtk.ListBoxRow()
		row_alignment = Gtk.Alignment()
		row_alignment.set_padding(8, 8, 4, 4)
		row_alignment.add(row)
		min_size_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=48)
		row.add(min_size_box)
		min_size_label = Gtk.Label(xalign=0)
		min_size_label.set_text("Min size")
		self.min_size_view = FileSizeUnitsView()
		min_size_box.pack_start(min_size_label, True, True, 0)
		min_size_box.pack_end(self.min_size_view, False, True, 0)
		self.left_panel.add(row_alignment)

		# Min size
		row = Gtk.ListBoxRow()
		row_alignment = Gtk.Alignment()
		row_alignment.set_padding(8, 8, 4, 4)
		row_alignment.add(row)
		owner_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=48)
		row.add(owner_box)
		owner_label = Gtk.Label(xalign=0)
		owner_label.set_text("Owner")
		self.owner_entry = Gtk.Entry(xalign=1)
		owner_box.pack_start(owner_label, True, True, 0)
		owner_box.pack_end(self.owner_entry, False, True, 0)
		self.left_panel.add(row_alignment)

		# Search result view
		self.result_list = SearchResultView()

		self.scrolled_window = Gtk.ScrolledWindow()
		self.scrolled_window.set_hexpand(True)
		self.scrolled_window.set_min_content_width(300)
		self.scrolled_window.set_vexpand(True)
		self.scrolled_window.add(self.result_list)
		self.scrolled_window.set_margin_bottom(0)
		self.right_panel.pack_start(self.scrolled_window, True, True, 0)
		self.progress_bar = Gtk.ProgressBar()

		self.timeout_id = GObject.timeout_add(50, self.on_timeout, None)

		self.status_bar = Gtk.Statusbar()
		self.context_id = self.status_bar.get_context_id("search_cid")
		self.status_bar.push(self.context_id, "Searching is fun!")
		self.status_bar.set_margin_bottom(0)
		self.status_bar.set_margin_top(0)
		self.status_bar.set_margin_left(0)

		self.main_panel = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0, homogeneous=False)

		# Scrolled window for the left panel
		left_scrolled_window = Gtk.ScrolledWindow()
		left_scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		left_scrolled_window.set_hexpand(False)
		left_scrolled_window.set_vexpand(True)
		left_scrolled_window.add(self.left_panel)

		self.main_panel.pack_start(left_scrolled_window, False, True, 12)
		self.main_panel.pack_start(self.right_panel, True, True, 0)

		self.pack_start(h_box, False, True, 8)
		self.pack_start(self.main_panel, True, True, 0)

		self.pack_start(self.progress_bar, False, True, 0)
		self.progress_bar.pulse()

		self.pack_start(self.status_bar, False, False, 0)

	def on_ignore_case_changed(self, switch, gparam):
		ignore_case_value = switch.get_active()
		self.ignoreCase = ignore_case_value

	def on_button_toggled(self, button, name):
		active_value = button.get_active()

		if name == "file":
			self.searchFile = active_value
		elif name == "folder":
			self.searchDirectory = active_value
		if name == "link":
			self.searchLink = active_value

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
		simple_search(query=self.entry.get_text(), path=self.searchPath, thread=self.thread, result_list=self.result_list, completed_function=self.search_complete, ignore_case=self.ignoreCase,
		              search_file=self.searchFile, search_folder=self.searchDirectory, search_link=self.searchLink, max_size=self.max_size_view.get_size_byte(), min_size=self.min_size_view.get_size_byte(), owner=self.owner_entry.get_text())

	def search_complete(self):
		self.progress_bar.hide()

		self.search_button.show()
		self.cancel_button.hide()

		if self.thread.stopped():
			self.status_bar.push(self.context_id, "Search Canceled: %s results" % self.result_list.get_number_of_results())
		else:
			self.status_bar.push(self.context_id, "Search Completed: %s results" % self.result_list.get_number_of_results())

		self.result_list.set_is_searching(False)

	def on_folder_clicked(self, widget):
		dialog = Gtk.FileChooserDialog("Choose a folder", self.gtk_window, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))
		dialog.set_default_size(500, 300)

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			self.folder_button.set_label("Path: " + os.path.split(dialog.get_filename())[1])
			self.searchPath = dialog.get_filename()

		dialog.destroy()

	def after_show(self):
		self.cancel_button.hide()
		self.progress_bar.hide()
