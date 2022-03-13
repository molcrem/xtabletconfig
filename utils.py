import subprocess
from tcclasses import *

# return the dimensions a_size as resized to have height and width fit within
#	or to b_size
def calculate_fit_a_in_b(a_size, b_size):
	a_width = a_size[0]
	a_height = a_size[1]
	b_width = b_size[0]
	b_height = b_size[1]
	a_aspect = a_width / a_height
	b_aspect = b_width / b_height
	
	new_a_width=None
	new_a_height=None
	
	# b's aspect ratio is wider than a's aspect ratio so fit a to height of b
	if b_aspect > a_aspect:
		new_a_height = b_height
		new_a_width = b_height * a_aspect
		new_a_height = b_height
	# b's aspect ratio is narrower than a's aspect ratio so fit a to width of b
	elif b_aspect < a_aspect:
		new_a_width = b_width
		new_a_height = b_width / a_aspect
		
	else:
		new_a_width = b_width
		new_a_height = b_height
	
	return [new_a_width, new_a_height]

def calculate_fit_a_in_b_normalized(a_size, b_size):
	new_a_size = None
	new_b_size = None
	
	print("b_size:", b_size[0], b_size[1])
	
	new_a_size = calculate_fit_a_in_b(a_size, b_size)
	print("new_a_size:", new_a_size[0], new_a_size[1])
	
	new_a_size = normalize_dimensions(new_a_size)
	print("new_a_size:", new_a_size[0], new_a_size[1])
	return new_a_size

# use xrandr to get information about connected displays
def get_display_info():
	displays = []
	ret = subprocess.run(["xrandr", "--listmonitors"], capture_output=True,
		text=True
	)
	lines = ret.stdout.splitlines()
	lines.pop(0)
	for line in lines:
		display = process_xrandr_line(line)
		if display:
			displays.append(display)
	
	if len(displays) > 0:
		return displays
	else:
		return False

# get a list of pointer device names and ids
def get_input_device_info():
	# create a list to store device id to device name mappings
	devices = list()
	
	# use xinput to get list of ids
	idsret = subprocess.run(
		["xinput", "list", "--id-only"], capture_output=True, text=True
	)
	ids = idsret.stdout.splitlines()
	
	# use the list of ids to get the device name related to each device id using
	#	"xinput list-props [id]"
	for id in ids:
		# get the device name using the id
		
		# get the xinput list-props output
		listpropsret = subprocess.run(["xinput", "list-props", id],
			capture_output=True, text=True
		)
			
		# we will assume that the first line of the output is the line that
		#	contains the device name info
		# ideally we would test to make sure the line started with "Device '"
		#	to check that it was the line we are expecting, however i have no
		#	idea if or how the output of xinput might change depending on
		#	things like user language settings and i don't care to spend time
		#	researching that either
		line = (listpropsret.stdout.splitlines())[0]
		
		tline = line
		
		# get the index of the positions after the first occurance of ' in line 
		#	in a forward search
		index = tline.index("'") + 1
		
		# get the contents of the line starting from index
		tline = tline[index:]
		
		# reverse tline
		tline = "".join(reversed(tline))
		
		# remove the first occurance of ' in the reversed in a forward search
		index = tline.index("'") + 1
		tline = tline[index:]
		
		# unreverse the line to get our final device name
		dname = ''.join(reversed(tline))
		
		# check to see wether or not the current device id is for a pointer
		#	device, since we are only interested in pointer devices
		
		# get info about device using output from "xinput list [id]"
		listret = subprocess.run(["xinput", "list", id],
			capture_output=True, text=True
		)
		grepret = subprocess.run(["grep", "pointer"], input=listret.stdout,
			capture_output=True, text=True
		)
		
		# a line containing "pointer" was found by grep so this is probably
		#	a pointer device
		if(len(grepret.stdout.splitlines()) > 0):
			devices.append({"id": id, "name": dname})
		
	return devices

def get_input_info_old():
	#ret = subprocess.run(
	#	["bash", "$(xinput | grep pointer | grep slave | grep -v Virtual)"],
	#	capture_output=True, text=True
	#)
	ret = subprocess.run("xinput", capture_output=True, text=True)
	ret = subprocess.run(["grep", "pointer"], input=ret.stdout,
		capture_output=True, text=True)
	ret = subprocess.run(["grep", "-v", "Virtual"], input=ret.stdout,
		capture_output=True, text=True)
	
	lines = ret.stdout.splitlines()
	for line in lines:
		split1 = line.split()
		print("line:", split1)
	
	return

# this function assumes there is only one screen, since this program is not
#	currently designed to support more than one screen.
def get_screen_info():
	ret = subprocess.run("xrandr", capture_output=True, text=True)
	
	# line is expected to be formatted like:
	#	Screen 0: minimum 8 x 8, current 4480 x 1200, maximum 16384 x 16384
	line = ret.stdout.splitlines()[0]
	
	# chunks would be expected to be:
	#	['Screen 0: minimum 8 x 8', 'current 4480 x 1200', 
	#		'maximum 16384 x 16384'
	#	]
	chunks = line.split(", ")
	
	# get the width and height from the chunk 'current 4480 x 1200'
	screen_width = chunks[1].split()[1]
	screen_height = chunks[1].split()[3]
	
	return [screen_width, screen_height]

def normalize_dimensions(a_size):
	new_a_size = [0, 0]
	
	if a_size[0] > a_size[1]:
		new_a_size[0] = 1
		new_a_size[1] = a_size[1] / a_size[0]
	elif a_size[0] < a_size[1]:
		new_a_size[0] = a_size[0] / a_size[1]
		new_a_size[1] = 1
	else:
		new_a_size[0] = 1
		new_a_size[1] = 1
		
	return new_a_size

"""
def process_xinput_line(line):
	items = line.split()
"""

# retrieve usable data from the passed xrandr output string
# splits the string into smaller strings using known characters used in xrandr
#	output as the split points until we're left with the individual values we
#	want
def process_xrandr_line(line):
	items = line.split()
	
	if len(items) != 4:
		return False
	
	data = items[2]
	
	split1 = data.split('x')
	if len(split1) != 2:
		print("split1")
		return False
	
	split2 = split1[1].split('+')
	if len(split2) != 3:
		print("split2")
		return False
	
	split3 = split1[0].split('/')
	if len(split3) != 2:
		print("split3")
		return False
	
	split4 = split2[0].split('/')
	if len(split4) != 2:
		print("split4")
		return False
	
	adapter = items[3]
	resx = int(split3[0])
	resy = int(split4[0])
	dimensionx = int(split3[1])
	dimensiony = int(split4[1])
	offsetx = int(split2[1])
	offsety = int(split2[2])
	
	display = Display(
		adapter, [resx, resy], [dimensionx, dimensiony], [offsetx, offsety]
	)
	
	return display

def scale_of_a_fit_in_b(a_size, b_size):
	new_a_size = calculate_fit_a_in_b(a_size, b_size)
	new_a_scale = new_a_size[0] / a_size[0]
	return new_a_scale
	