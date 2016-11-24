import os

import gi
import subprocess

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk


class SearchResultWidget(Gtk.TreeView):
	def __init__(self):
		self.liststore = Gtk.ListStore(str, str, str, str)
		Gtk.Window.__init__(self, model=self.liststore)

		renderer_pixbuf = Gtk.CellRendererPixbuf()
		column_pixbuf = Gtk.TreeViewColumn("", renderer_pixbuf, icon_name=0)
		column_pixbuf.set_sort_column_id(0)
		self.append_column(column_pixbuf)

		renderer_name = Gtk.CellRendererText()
		column_name = Gtk.TreeViewColumn("Name", renderer_name, text=2)
		column_name.set_sort_column_id(2)
		self.set_default_column_properties(column_name)
		self.append_column(column_name)

		renderer_path = Gtk.CellRendererText()
		column_path = Gtk.TreeViewColumn("Path", renderer_path, text=1)
		column_path.set_sort_column_id(1)
		self.set_default_column_properties(column_path)
		self.append_column(column_path)

		renderer_size = Gtk.CellRendererText()
		column_size = Gtk.TreeViewColumn("Size", renderer_size, text=3)
		column_size.set_sort_column_id(3)
		self.set_default_column_properties(column_size)
		self.append_column(column_size)
		self.connect('button-press-event', self.button_press_event)

	def addItem(self, search_result):
		result_array = search_result.toArray()
		result_array[0] = Gio.content_type_get_icon(result_array[0]).get_names()[0]
		self.liststore.append(result_array)

	def clear(self):
		self.liststore.clear()

	def set_default_column_properties(self, column):
		column.set_resizable(True)
		column.set_expand(True)
		column.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
		column.set_fixed_width(True)

	# column.set_sort_indicator(True)


	def button_press_event(self, widget, event):
		if event.button == 3:  # right click
			tree_path = self.get_path_at_pos(int(event.x), int(event.y))[0]
			menu = Gtk.Menu()

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
		path = self.liststore.get_value(self.liststore.get_iter(tree_path), 1)
		name = self.liststore.get_value(self.liststore.get_iter(tree_path), 2)
		file_path = os.path.join(path, name)
		print("file clicked path: " + file_path)
		p = subprocess.Popen(['nautilus', file_path])

	def xdg_open_file(self, widget, tree_path):
		path = self.liststore.get_value(self.liststore.get_iter(tree_path), 1)
		name = self.liststore.get_value(self.liststore.get_iter(tree_path), 2)
		file_path = os.path.join(path, name)
		print("file clicked path: " + file_path)
		p = subprocess.Popen(['xdg-open', file_path])

	def copy_path(self, widget, tree_path):
		path = self.liststore.get_value(self.liststore.get_iter(tree_path), 1)
		name = self.liststore.get_value(self.liststore.get_iter(tree_path), 2)
		file_path = os.path.join(path, name)
		Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD).set_text(file_path, -1)
