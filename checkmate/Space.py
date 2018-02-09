import checkmate as cm

class Space:
	def __init__(self, xy, colour):
		assert colour in ['black', 'white'], 'Invalid colour for Space object'
		self.colour = colour
		x, y = xy
		self.x, self.y = x, y
		self.xy = (x, y)
		self.x_name, self.y_name = cm.xy_to_board(xy)
		self.held_by = None

	def occupy(self, Piece):
		self.held_by = Piece

	def vacate(self):
		self.held_by = None

	def get_Piece(self):
		return self.held_by

	def __str__(self):
		return 'Space '+ str(self.x_name) + str(self.y_name) + ' ('+self.colour+')'

	def __repr__(self):
		return self.__str__()