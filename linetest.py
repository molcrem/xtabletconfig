line = "Device '     Union's PF20's Super's':"

tline = line

# get the index of the positions after the first occurance of ' in line in a
#	forward search
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

print("dname:", name)

"""
squote_count = line.count("'")

print("line", line)
print("squote_count:", squote_count)
print("")

# create a copy of line that we will repeatedly remove the first occuring chunk
#	of text ending with a ' from our text line
# the idea is to remove more and more sections of text until we reach the last
#	occuring ' in the text line
tline = line

# chunks of text wil be added together while iterating through the line until we
#	find the last ', indicating the end of the outputted device name string
name = ""
for i in range(0, squote_count):
	print(i)
	print("tline:", tline)
	
	# get the index for character after the first ' appares in current tline
	index = tline.index("'") + 1
	tline = tline[index:]
	
	if i > 0:
		name += 
	
	
	print("tline:", tline)
	print("")
"""