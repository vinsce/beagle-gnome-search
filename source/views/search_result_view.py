import os

import gi
import subprocess

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk


class SearchResultView(Gtk.TreeView):
	def __init__(self):
		self.list_store = Gtk.ListStore(str, str, str, str)
		Gtk.TreeView.__init__(self, model=self.list_store)

		# File icon column
		renderer_pixbuf = Gtk.CellRendererPixbuf()
		column_pixbuf = Gtk.TreeViewColumn("", renderer_pixbuf, icon_name=0)
		self.append_column(column_pixbuf)

		# File name column
		renderer_name = Gtk.CellRendererText()
		column_name = Gtk.TreeViewColumn("Name", renderer_name, text=2)
		column_name.set_sort_column_id(2)
		self.set_default_column_properties(column_name)
		self.append_column(column_name)

		# File path column
		renderer_path = Gtk.CellRendererText()
		column_path = Gtk.TreeViewColumn("Path", renderer_path, text=1)
		column_path.set_sort_column_id(1)
		self.set_default_column_properties(column_path)
		self.append_column(column_path)

		# File size column
		renderer_size = Gtk.CellRendererText()
		column_size = Gtk.TreeViewColumn("Size", renderer_size, text=3)
		column_size.set_sort_column_id(3)
		self.list_store.set_sort_func(3, self.size_sort_func)
		self.set_default_column_properties(column_size)
		self.append_column(column_size)

		# Attach a listener to capture the right mouse button click event
		self.connect('button-press-event', self.button_press_event)

	@staticmethod
	def get_byte_file_size(file_size_string):
		byte_size = 0
		if file_size_string.endswith("PB"):
			byte_size = float(file_size_string[:-2]) * (2 ** 50)
		elif file_size_string.endswith("TB"):
			byte_size = float(file_size_string[:-2]) * (2 ** 40)
		elif file_size_string.endswith("GB"):
			byte_size = float(file_size_string[:-2]) * (2 ** 30)
		elif file_size_string.endswith("MB"):
			byte_size = float(file_size_string[:-2]) * (2 ** 20)
		elif file_size_string.endswith("KB"):
			byte_size = float(file_size_string[:-2]) * (2 ** 10)
		elif file_size_string.endswith("B"):
			byte_size = float(file_size_string[:-1])
		return byte_size

	def size_sort_func(self, model, row1, row2, user_data):
		""" custom function for file sorting using the file size """
		sort_column = 3

		value1 = model.get_value(row1, sort_column)
		value2 = model.get_value(row2, sort_column)

		num_v1 = self.get_byte_file_size(value1)
		num_v2 = self.get_byte_file_size(value2)

		if num_v1 < num_v2:
			return -1
		elif num_v1 == num_v2:
			return 0
		else:
			return 1

	def add_search_result(self, search_result):
		result_array = search_result.to_array()
		result_array[0] = Gio.content_type_get_icon(result_array[0]).get_names()[0]
		self.list_store.append(result_array)

	def clear(self):
		self.list_store.clear()

	@staticmethod
	def set_default_column_properties(column):
		column.set_resizable(True)
		column.set_expand(True)
		column.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
		column.set_fixed_width(True)

	def button_press_event(self, widget, event):
		if event.button == 3:  # right button click event
			tree_path = self.get_path_at_pos(int(event.x), int(event.y))[0]

			# creates and shows a popup menu
			menu = Gtk.Menu()
			menu.attach_to_widget(widget)

			menu_item_nautilus = Gtk.MenuItem("Show in Nautilus")
			menu_item_nautilus.connect("activate", self.open_nautilus, tree_path)
			menu.append(menu_item_nautilus)
			menu_item_nautilus.show()

			menu_item_open = Gtk.MenuItem("Open file")
			menu_item_open.connect("activate", self.xdg_open_file, tree_path)
			menu.append(menu_item_open)
			menu_item_open.show()

			menu_item_copy_path = Gtk.MenuItem("Copy path")
			menu_item_copy_path.connect("activate", self.copy_path, tree_path)
			menu.append(menu_item_copy_path)
			menu_item_copy_path.show()

			menu.popup(parent_menu_shell=None, parent_menu_item=None, func=None, data=None, button=event.button, activate_time=event.time)

	def open_nautilus(self, widget, tree_path):
		path = self.list_store.get_value(self.list_store.get_iter(tree_path), 1)
		name = self.list_store.get_value(self.list_store.get_iter(tree_path), 2)
		file_path = os.path.join(path, name)
		subprocess.Popen(['nautilus', file_path])

	def xdg_open_file(self, widget, tree_path):
		path = self.list_store.get_value(self.list_store.get_iter(tree_path), 1)
		name = self.list_store.get_value(self.list_store.get_iter(tree_path), 2)
		file_path = os.path.join(path, name)
		subprocess.Popen(['xdg-open', file_path])

	def copy_path(self, widget, tree_path):
		path = self.list_store.get_value(self.list_store.get_iter(tree_path), 1)
		name = self.list_store.get_value(self.list_store.get_iter(tree_path), 2)
		file_path = os.path.join(path, name)
		Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD).set_text(file_path, -1)
