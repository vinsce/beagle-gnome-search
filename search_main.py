from views.search_main_window import SearchMainWindow
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

win = SearchMainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()

win.after_show()

Gtk.main()
