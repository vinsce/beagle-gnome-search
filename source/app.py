import os
import sys

import gi

from views.search_main_window import SearchMainWindow

gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk


class Application(Gtk.Application):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, application_id="org.storyteller.gsearch", flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE, **kwargs)
		self.window = None

		self.add_main_option("base", ord("b"), GLib.OptionFlags.NONE, GLib.OptionArg.NONE, "Open directly the base search screen", None)

	def do_startup(self):
		Gtk.Application.do_startup(self)

		action = Gio.SimpleAction.new("about", None)
		action.connect("activate", self.on_about)
		self.add_action(action)

		action = Gio.SimpleAction.new("quit", None)
		action.connect("activate", self.on_quit)
		self.add_action(action)

		action = Gio.SimpleAction.new("preferences", None)
		action.connect("activate", self.on_preferences)
		# self.add_action(action)
		builder = Gtk.Builder.new_from_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "res", "xml", "app_menu.xml"))
		self.set_app_menu(builder.get_object("app-menu"))

	def do_activate(self):
		if not self.window:
			self.window = SearchMainWindow(application=self, title="Main Window")
		self.window.present()

	def do_command_line(self, command_line):
		options = command_line.get_options_dict()

		if options.contains("base"):
			# TODO This will be used to show the right search page: base, simple, etc
			print("Base argument recieved")

		self.activate()
		return 0

	# Functions used to handle top menu actions: about, quit and preferences
	def on_about(self, action, param):
		about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True, authors=["<a href=\"mailto:vincenzo.cerminara94@gmail.com\">Vincenzo Cerminara</a>"], comments="A multiversal search tool for GNOME.",
		                               version="0.1", program_name="GSearch")
		about_dialog.present()

	def on_quit(self, action, param):
		self.quit()

	def on_preferences(self, action, param):
		# TODO add preference dialog
		pass


if __name__ == "__main__":
	app = Application()
	app.run(sys.argv)
