import checkmate as cm

class Game:
	def __init__(self):
		self.gameboard = cm.Board()
		self.gameboard.setup_Game()
		self.all_piece_types = ('pawn', 'bishop', 'rook', 'knight', 'king', 'queen')
		self.all_colours = ('black', 'white')

	def __str__(self):
		return self.gameboard.__str__()

	def __repr__(self):
		return self.gameboard.__repr__()