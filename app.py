import sys

import gi

from views.search_main_window import SearchMainWindow

gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk


class Application(Gtk.Application):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, application_id="org.example.myapp", flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE, **kwargs)
		self.window = None

		self.add_main_option("test", ord("t"), GLib.OptionFlags.NONE, GLib.OptionArg.NONE, "Command line test", None)

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
		#self.add_action(action)

		builder = Gtk.Builder.new_from_file("res/xml/app_menu.xml")
		self.set_app_menu(builder.get_object("app-menu"))

	def do_activate(self):
		# We only allow a single window and raise any existing ones
		if not self.window:
			# Windows are associated with the application
			# when the last one is closed the application shuts down
			self.window = SearchMainWindow(application=self, title="Main Window")
			self.window.set_wmclass("Hello World", "Hello World")

		self.window.present()

	def do_command_line(self, command_line):
		options = command_line.get_options_dict()

		if options.contains("test"):
			# This is printed on the main instance
			print("Test argument recieved")

		self.activate()
		return 0

	def on_about(self, action, param):
		about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
		about_dialog.present()

	def on_quit(self, action, param):
		self.quit()

	def on_preferences(self, action, param):
		pass


if __name__ == "__main__":
	app = Application()
	app.run(sys.argv)
