class Display:
	def __init__(self, adapter, resolution, dimensions, offset):
		# [x, y]
		self.adapter = adapter
		# [x, y]
		self.resolution = resolution
		# [x, y]
		self.dimensions = dimensions
		# [x, y]
		self.offset = offset

class TabletInfo:
	def __init__(self, width=12, height=9):
		self.width = width
		self.height = height