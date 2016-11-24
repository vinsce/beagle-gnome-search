import signal

import gi, subprocess, os, threading

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GObject
from SearchResultWidget import SearchResultWidget
from search_result import SearchResult


class StoppableThread(threading.Thread):
	"""Thread class with a stop() method. The thread itself has to check regularly for the stopped() condition."""

	def __init__(self, target=None):
		super(StoppableThread, self).__init__(target=target)
		self._stop = threading.Event()

	def set_pid(self, pid):
		self.pid = pid

	def stop(self):
		self._stop = threading.Event()
		self._stop.set()
		if self.pid:
			print("pid: " + str(self.pid))
			os.kill(self.pid, signal.SIGTERM)

	def stopped(self):
		return self._stop.isSet()


class SearchMainWindow(Gtk.Window):
	def __init__(self):
		self.thread = StoppableThread(target=self.effectiveSearch)

		# Window configurations
		Gtk.Window.__init__(self, title="HeaderBar Demo")
		self.set_border_width(10)
		self.set_default_size(400, 200)
		self.searchPath = "/home/vinsce/Sviluppo"

		# Headerbar initialization
		hb = Gtk.HeaderBar()
		hb.set_show_close_button(True)

		# Stack initialization
		stack = Gtk.Stack()
		stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
		stack.set_transition_duration(1000)

		# First stack page (simple)
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.folderButton = Gtk.Button("Folder: " + self.searchPath)
		self.folderButton.connect("clicked", self.on_folder_clicked)
		self.entry = Gtk.SearchEntry()
		self.entry.set_text("test*")
		self.searchButton = Gtk.Button.new_from_icon_name("system-search-symbolic", Gtk.IconSize.BUTTON)
		self.searchButton.connect("clicked", self.executeSearch)

		self.cancelButton = Gtk.Button.new_from_icon_name("edit-clear-all-symbolic", Gtk.IconSize.BUTTON)
		self.cancelButton.connect("clicked", self.cancelSearch)

		hbox.pack_start(self.folderButton, False, True, 8)
		hbox.pack_start(self.entry, True, True, 8)
		hbox.pack_start(self.searchButton, False, True, 0)
		hbox.pack_start(self.cancelButton, False, True, 0)

		self.resultList = SearchResultWidget()
		vbox.pack_start(hbox, False, True, 8)

		self.searchResultLabel = Gtk.Label()
		self.searchResultLabel.set_markup("<big>Search Result</big>")
		self.scrolledwindow = Gtk.ScrolledWindow()
		self.scrolledwindow.set_hexpand(False)
		self.scrolledwindow.set_vexpand(True)
		self.scrolledwindow.add(self.resultList)
		vbox.pack_start(self.scrolledwindow, True, True, 0)

		self.progressbar = Gtk.ProgressBar()
		vbox.pack_start(self.progressbar, False, True, 0)
		self.progressbar.pulse()

		self.timeout_id = GObject.timeout_add(50, self.on_timeout, None)

		stack.add_titled(vbox, "base", "Base")

		# self.resultList.connect('size-allocate', self.treeview_changed)

		# Second stack page (advanced)
		label = Gtk.Label()
		label.set_markup("<big>A fancy label</big>")
		stack.add_titled(label, "advanced", "Advanced")

		# Setting stack switcher as headerbar title
		stack_switcher = Gtk.StackSwitcher()
		stack_switcher.set_stack(stack)
		hb.set_custom_title(stack_switcher)
		self.set_titlebar(hb)

		# Headerbar right buttons
		button = Gtk.Button()
		icon = Gio.ThemedIcon(name="mail-send-receive-symbolic")
		image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
		button.add(image)
		hb.pack_end(button)

		# Headerbar left buttons
		box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		Gtk.StyleContext.add_class(box.get_style_context(), "linked")
		button = Gtk.Button()
		button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
		box.add(button)
		button = Gtk.Button()
		button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
		box.add(button)
		hb.pack_start(box)

		# Add stack as window content
		self.add(stack)

	def on_timeout(self, user_data):
		self.progressbar.pulse()
		return True

	def executeSearch(self, button):

		self.searchButton.hide()
		self.cancelButton.show()

		self.resultList.clear()
		self.progressbar.show()

		self.thread = StoppableThread(target=self.effectiveSearch)
		self.thread.start()

	def cancelSearch(self, button):
		self.thread.stop()

	def treeview_changed(self, widget, event, data=None):
		adj = self.scrolledwindow.get_vadjustment()
		adj.set_value(adj.get_upper() - adj.get_page_size())

	def effectiveSearch(self):
		p = subprocess.Popen(["find", self.searchPath, "-iname", self.entry.get_text()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		self.thread.set_pid(p.pid)
		# out, err = p.communicate()
		# self.searchResultLabel.set_markup("Out: "+out.decode('utf-8') + "\nErr: "+err.decode('utf-8'))

		with p.stdout:
			for line in iter(p.stdout.readline, b''):
				file_name = line.rstrip().decode('utf-8')
				self.resultList.addItem(SearchResult(file_name))
				if self.thread.stopped():
					break
			p.wait()
			print("terminato")

		self.progressbar.hide()

		self.searchButton.show()
		self.cancelButton.hide()

	# if not err:
	# for file_name in out.splitlines():
	#	self.resultList.addItem(SearchResult(file_name.decode('utf-8')))

	def on_folder_clicked(self, widget):
		dialog = Gtk.FileChooserDialog("Please choose a folder", self, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
		                                                                                                     "Select", Gtk.ResponseType.OK))
		dialog.set_default_size(800, 400)

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			print("Select clicked")
			print("Folder selected: " + dialog.get_filename())
			self.folderButton.set_label("Path: " + os.path.split(dialog.get_filename())[1])
			self.searchPath = dialog.get_filename()
		elif response == Gtk.ResponseType.CANCEL:
			print("Cancel clicked")

		dialog.destroy()


win = SearchMainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()

win.cancelButton.hide()
win.progressbar.hide()

Gtk.main()
