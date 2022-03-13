import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from utils import *
from tcclasses import *

class MyWindow(Gtk.Window):
	def __init__(self, app, displays, tablet_info):
		Gtk.Window.__init__(self, title="Hello World")
		
		self.app = app
		self.tablet_info = tablet_info
		
		# main layout container
		self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing=4)
		self.box.set_margin_start(5)
		self.box.set_margin_top(5)
		self.box.set_margin_end(5)
		self.box.set_margin_bottom(5)
		self.add(self.box)
		self.device_cb = ""
		
		# select input device combo box
		if len(self.app.devices) > 0:
			self.device_cb_text_to_device = dict()
			self.device_cb = Gtk.ComboBoxText.new()
			
			# where the numbers will start in the numbered list of devices
			current_num = 1
			for device in self.app.devices:
				text = str(current_num) + ": " + device["name"]
				self.device_cb_text_to_device[text] = device
				self.device_cb.append_text(text)
				current_num += 1
			
			self.device_cb.set_active(0)
			self.device_cb.connect("changed", self.on_device_cb_changed)
			self.box.pack_start(self.device_cb, False, False, 0)
		else:
			print("error: could not get input devices info")
		
		# width section
		self.hbox_width = Gtk.HBox()
		self.box.pack_start(self.hbox_width, True, True, 0)
		
		self.entry_width = Gtk.Entry()
		self.entry_width.set_text(str(self.tablet_info.width))
		#self.entry_width.editing_done()
		self.hbox_width.pack_start(self.entry_width, True, True, 0)
		
		self.label_width = Gtk.Label(label="Tablet drawing area width")
		self.hbox_width.pack_start(self.label_width, True, True, 0)
		
		# height section
		self.hbox_height = Gtk.HBox()
		self.box.pack_start(self.hbox_height, True, True, 0)
		
		self.entry_height = Gtk.Entry()
		self.entry_height.set_text(str(self.tablet_info.height))
		self.hbox_height.pack_start(self.entry_height, True, True, 0)
		
		self.label_height = Gtk.Label(label="Tablet drawing area height")
		self.hbox_height.pack_start(self.label_height, True, True, 0)
		
		# monitor lock section
		self.label = Gtk.Label(
			label="Lock tablet area to the following monitor:"
		)
		self.box.pack_start(self.label, True, True, 0)
		
		# displays combo box
		self.cb = Gtk.ComboBoxText.new()
		for display in displays:
			if display.adapter:
				self.cb.append_text(display.adapter)
		self.cb.set_active(0)
		self.cb.connect("changed", self.on_cb_changed)
		self.box.pack_start(self.cb, False, False, 0)
		
		# submit button
		self.button = Gtk.Button(label="Click Here")
		self.button.connect("clicked", self.on_button_clicked)
		self.box.pack_start(self.button, False, False, 0)
		
		#self.button.grab_focus()
	
	def get_selected_device(self):
		active_cb_text = self.device_cb.get_active_text()
		device = self.device_cb_text_to_device[active_cb_text]
		return device
	
	# submit user provided data for handling
	def on_button_clicked(self, button):
		# get the device relating to the currently selected device combo box
		#	item
		device = self.get_selected_device()
		print("current device:", device)
	
		# check to make sure data in the entry boxes is numeric
		try:
			tablet_dimensions = [0, 0]
			tablet_dimensions[0] = float(self.entry_width.get_text())
			tablet_dimensions[1] = float(self.entry_height.get_text())
		except:
			print("error reading tablet width/height values from entry boxes")
			return False
		
		# check to make sure the entry box numeric data is good
		if not (tablet_dimensions[0] > 0 and tablet_dimensions[1] > 0):
			print("tablet width and height values must be non-zero, positive ",
				"numbers")
			return False
		
		# index of the selected item in the displays combo box
		active_index = self.cb.get_active()
		
		# no item selected in combo box
		if active_index < 0:
			print("error?: invalid current combo box item")
			return False
		
		self.app.on_set_mapping(tablet_dimensions, active_index)
	
	def on_cb_changed(self, cb):
		#print(cb)
		#print(cb.get_active_text())
		#print(cb.get_active(), "\n")
		pass
	
	def on_device_cb_changed(self, cb):
		print(cb.get_active_text())
		return

class App:
	def __init__(self):
		self.tablet_info = TabletInfo()
		self.displays = get_display_info()
		self.devices = get_input_device_info()
		self.current_device = ""
		self.screen_info = get_screen_info()
		
		"""
		for display in self.displays:
			print("adapter:", display.adapter)
			print("resolution:", display.resolution)
			print("dimensions:", display.dimensions)
			print("offset:", display.offset)
			print("")
		"""
		
		win = MyWindow(self, self.displays, self.tablet_info)
		win.connect("destroy", Gtk.main_quit)
		win.show_all()
		
		Gtk.main()
	
	# respond to gui submission by trying to set the tablet settings according
	#	to the user submitted data
	def on_set_mapping(self, tablet_dimensions, display_index):
		# bad display combo box entry sent
		if not (display_index >= 0 and display_index <= len(self.displays)):
			return False
		
		# calculate tablet aspect ratio
		aspect_ratio = tablet_dimensions[1] / tablet_dimensions[0]
		
		# get the relevant display using display_index
		display = self.displays[display_index]
		
		print("display resolution:")
		print(display.resolution[0], display.resolution[1])
		print("tablet dimensions:")
		print(tablet_dimensions[0], tablet_dimensions[1])
		print("tablet aspect ratio:")
		print(aspect_ratio)
		
		# figure out the resolution of the desktop space
		
		
		
		# calculate the tablet transform scale
		tablet_scale = calculate_fit_a_in_b_normalized(tablet_dimensions, 
			display.resolution
		)
		
		print("tablet scale:", tablet_scale[0], tablet_scale[1])

app = App()
