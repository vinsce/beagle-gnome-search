import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

unit_mult = {"byte": 1, "kb": 1024, "mb": 1048576, "gb": 1073741824}


class FileSizeUnitsView(Gtk.Box):
	""" view that displays an entry for size input and 4 buttons to choose the size unit """

	def __init__(self):
		super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=4, homogeneous=False)

		self.size_entry = Gtk.Entry(xalign=1)
		self.size_entry.set_width_chars(5)
		self.pack_start(self.size_entry, True, False, 0)

		buttons_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

		button_byte = Gtk.RadioButton.new_with_label_from_widget(None, "B")
		button_byte.connect("toggled", self.on_button_toggled, "byte")
		button_byte.set_mode(False)
		buttons_box.pack_start(button_byte, True, True, 0)

		button_kilo = Gtk.RadioButton.new_from_widget(button_byte)
		button_kilo.set_label("KB")
		button_kilo.connect("toggled", self.on_button_toggled, "kb")
		button_kilo.set_mode(False)
		buttons_box.pack_start(button_kilo, True, True, 0)

		button_mega = Gtk.RadioButton.new_from_widget(button_byte)
		button_mega.set_label("MB")
		button_mega.connect("toggled", self.on_button_toggled, "mb")
		button_mega.set_mode(False)
		buttons_box.pack_start(button_mega, True, True, 0)

		button_giga = Gtk.RadioButton.new_from_widget(button_byte)
		button_giga.set_label("GB")
		button_giga.connect("toggled", self.on_button_toggled, "gb")
		button_giga.set_mode(False)
		buttons_box.pack_start(button_giga, True, True, 0)

		self.pack_start(buttons_box, False, False, 0)

		button_kilo.set_active(True)
		self.selected_unit = "kb"

	def on_button_toggled(self, button, value):
		self.selected_unit = value

	def get_size_byte(self):
		try:
			return int(self.size_entry.get_text()) * unit_mult[self.selected_unit]
		except ValueError:
			self.size_entry.set_text("")
			return 0