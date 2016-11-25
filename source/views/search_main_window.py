import os

import gi

from views.searchpages import base, simple

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk


class SearchMainWindow(Gtk.ApplicationWindow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.thread = None

		# Window configurations
		self.set_border_width(0)
		self.set_default_size(800, 500)

		# Headerbar initialization
		hb = Gtk.HeaderBar()
		hb.set_show_close_button(True)

		# Stack initialization
		stack = Gtk.Stack()
		stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
		stack.set_transition_duration(1000)

		# First stack page (base)
		self.base_page = base.BaseSearchPage(gtk_window=self)
		stack.add_titled(self.base_page, "base", "Base")

		self.simple_page = simple.SimpleSearchPage(gtk_window=self)
		stack.add_titled(self.simple_page, "simple", "Simple")

		# Setting stack switcher as headerbar title
		stack_switcher = Gtk.StackSwitcher()
		stack_switcher.set_stack(stack)
		hb.set_custom_title(stack_switcher)
		self.set_titlebar(hb)

		# Add stack as window content
		self.add(stack)

		# self.connect("delete-event", Gtk.main_quit)
		self.show_all()

		self.after_show()

	def after_show(self):
		""" performs same initializations operation. It must be called after SearchMainWindow.show_all()"""
		self.base_page.after_show()
		self.simple_page.after_show()
