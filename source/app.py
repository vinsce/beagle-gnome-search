import os
import sys

import gi

from views.search_main_window import SearchMainWindow

gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk


class Application(Gtk.Application):
	def __init__(self, *args, **kwargs):
		super().__init__(application_id="me.storyteller.gsearch", flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE, *args, **kwargs)

		self.default_search_page = "base"
		self.window = None

		self.add_main_option("base", ord("b"), GLib.OptionFlags.NONE, GLib.OptionArg.NONE, "Open directly the base search screen", None)
		self.add_main_option("simple", ord("s"), GLib.OptionFlags.NONE, GLib.OptionArg.NONE, "Open directly the simple search screen", None)

	def do_startup(self):
		Gtk.Application.do_startup(self)

		about_action = Gio.SimpleAction.new("about", None)
		about_action.connect("activate", self.on_about)
		self.add_action(about_action)

		quit_action = Gio.SimpleAction.new("quit", None)
		quit_action.connect("activate", self.on_quit)
		self.add_action(quit_action)

		preferences_action = Gio.SimpleAction.new("preferences", None)
		preferences_action.connect("activate", self.on_preferences)
		# self.add_action(preferences_action)

		# Loading menu from res/xml/app_menu.xml
		builder = Gtk.Builder.new_from_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "res", "xml", "app_menu.xml"))
		self.set_app_menu(builder.get_object("app-menu"))

	def do_activate(self):
		# Allows only one window instance
		if not self.window:
			self.window = SearchMainWindow(application=self, title="Search", page=self.default_search_page)
		self.window.present()

	def do_command_line(self, command_line):
		options = command_line.get_options_dict()

		# shows the right search page: base, simple, etc
		if options.contains("base"):
			self.default_search_page = "base"
		elif options.contains("simple"):
			self.default_search_page = "simple"

		self.activate()
		return 0

	# Functions used to handle top menu actions: about, quit and preferences
	def on_about(self, action, param):
		about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True, authors=["<a href=\"mailto:vincenzo.cerminara94@gmail.com\">Vincenzo Cerminara</a>"], comments="A search tool for GNOME.", version="0.1",
		                               program_name="GSearch")
		about_dialog.present()

	def on_quit(self, action, param):
		self.quit()

	def on_preferences(self, action, param):
		# TODO add preference dialog
		pass


if __name__ == "__main__":
	app = Application()
	app.run(sys.argv)
