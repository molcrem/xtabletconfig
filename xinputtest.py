import subprocess

def get_input_info_old():
	#ret = subprocess.run(
	#	["bash", "$(xinput | grep pointer | grep slave | grep -v Virtual)"],
	#	capture_output=True, text=True
	#)
	xlistret = subprocess.run("xinput", capture_output=True, text=True)
	greppointerlistret = subprocess.run(["grep", "pointer"], 
		input=xlistret.stdout, capture_output=True, text=True)
	
	lines = greppointerlistret.stdout.splitlines()
	for line in lines:
		#split1 = line.split()
		#print("line:", split1)
		print("line:")
		print(line)
		print("split line:")
		sline = line.split()
		print(sline)
		print("")
	
	#lines = ret.stdout.splitlines()
	#for line in lines:
	#	#split1 = line.split()
	#	#print("line:", split1)
	#	print(line)
	
	return

def get_input_info():
	# create a list to store device id to device name mappings
	devices = list()
	
	# use xinput to get list of ids
	idsret = subprocess.run(["xinput", "list", "--id-only"], capture_output=True, text=True)
	ids = idsret.stdout.splitlines()
	
	
	# use the list of ids to get the device name related to each device id using
	#	"xinput list-props [id]"
	for id in ids:
		#print("id:", id)
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
		
		#print("line:", line)
		
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

		#print("dname:", dname)
		
		# check to see wether or not the current device id is for a pointer
		#	device, since we are only interested in pointer devices
		
		# get info about device using output from "xinput list [id]"
		listret = subprocess.run(["xinput", "list", id],
			capture_output=True, text=True
		)
		grepret = subprocess.run(["grep", "pointer"], input=listret.stdout,
			capture_output=True, text=True
		)
		
		#print("grepret:")
		#print(grepret.stdout)
		#print("len:")
		#print(len(grepret.stdout.splitlines()))
		
		# a line containing "pointer" was found by grep so this is probably
		#	a pointer device
		if(len(grepret.stdout.splitlines()) > 0):
			devices.append({"id": id, "name": dname})
		
		#print("------")
	
	#print("devices:")
	#print(devices)
	
	return

get_input_info()