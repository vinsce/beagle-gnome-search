import gi

from views.searchpages import base, simple

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk


class SearchMainWindow(Gtk.ApplicationWindow):
	def __init__(self, page="base", *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.thread = None
		self.default_page = page

		# Window configurations
		self.set_border_width(0)
		self.set_default_size(800, 500)

		# HeaderBar initialization
		hb = Gtk.HeaderBar()
		hb.set_show_close_button(True)

		# Stack initialization
		self.stack = Gtk.Stack()
		self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
		self.stack.set_transition_duration(800)

		# First stack page (base)
		self.base_page = base.BaseSearchPage(gtk_window=self)
		self.stack.add_titled(self.base_page, "base", "Base")

		self.simple_page = simple.SimpleSearchPage(gtk_window=self)
		self.stack.add_titled(self.simple_page, "simple", "Simple")

		# Setting stack switcher as HeaderBar title
		stack_switcher = Gtk.StackSwitcher()
		stack_switcher.set_stack(self.stack)
		hb.set_custom_title(stack_switcher)
		self.set_titlebar(hb)

		# Add stack as window content
		self.add(self.stack)

		# Show the window
		self.show_all()
		self.after_show()

	def after_show(self):
		""" performs some initializations operation. It must be called after SearchMainWindow.show_all()"""
		if self.default_page == "base":
			self.stack.set_visible_child(self.base_page)
		elif self.default_page == "simple":
			self.stack.set_visible_child(self.simple_page)

		self.base_page.after_show()
		self.simple_page.after_show()