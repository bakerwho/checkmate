class Piece:
	def __init__(self, piece_type, piece_colour, Space = None, Space_warning = False):
		assert piece_colour.lower() in ['black', 'white'], 'Invalid colour'
		assert piece_type.lower() in ['pawn', 'bishop', 'rook', 'knight', 'king', 'queen'], 'Invalid piece_type'
		self.type = piece_type
		self.colour = piece_colour
		if Space is None and Space_warning:
			print('Warning : Space initialised as None')
		self.Space = Space

	def set_Space(self, Space):
		self.Space = Space

	def get_Space(self):
		return self.Space

	def get_legal_Moves(self, Board):
		this_Space = self.get_Space
		x, y = this_Space.x, this_Space.y
		assert Board[x][y].occupied_by_Piece == self

	def __str__(self):
		rep = 'Piece(' + str(self.type) + ', ' + str(self.colour) + ') at '





class Board:
	def __init__(self):
		colours = ('black', 'white')
		self.board = [[Space(i, j, colours[(i+j)%2]) for i in range(8)] for j in range(8)]
		self.free_spaces = [[(i, j) for i in range(8)] for j in range(8)]
		self.occupied_spaces = []

	def setup_Game(self, lower = 'white'):
		order = {'white' : 0, 'black' : 1}[lower]
		colours = [('white', 'black'), ('black', 'white')][order]
		pieces = [('rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook'), ('rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook')][order]
		for colour_no in range(len(colours)):
			colour = colours[colour_no]
			for y in range(8):
				x = colour_no * 5 + 1
				self.add_Piece('pawn', colour, (x, y))
			for y in range(len(pieces)):
				x = colour_no*7
				self.add_Piece(pieces[y], colour, (x, y))
	
	def add_Piece(self, piece_type, colour, xy):
		new_Piece = Piece(piece_type, colour)
		x, y = xy
		self.board[x][y].occupy(new_Piece)

	def get_all_Pieces(self):
		all_Pieces = {}
		for row in self.board:
			for Space in row:
				Piece = Space.get_Piece()
				if Piece is not None:
					print(type(Piece), Space)
					piece_name = Piece.colour + ' ' + Piece.type
					all_Pieces[piece_name] = Piece
		return all_Pieces

	def move_Piece(self, Piece, new_Space):
		pass


	def clear_Board(self):
		self.__init__()

	def __str__(self):
		rep = '\t ' + '_'*79+ '\n'
		breaker =  ['\t|'+''.join(['         |*********|' for i in range(4)]) + '\n' + 
					'\t|'+''.join(['_________|_________|' for i in range(4)]) + '\n', 
					'\t|'+''.join(['*********|         |' for i in range(4)]) + '\n' + 
					'\t|'+''.join(['_________|_________|' for i in range(4)]) + '\n']
		for i in range(len(self.board), 0, -1):
			row = self.board[i-1]
			rep_row = str(i) + '\t'
			for j in range(len(row)):
				Space = row[j]
				if Space.held_by is not None:
					rep_row += '| '+str(Space.held_by.colour[0] + ' ' + Space.held_by.type).ljust(8)
				else:
					rep_row += '| '+' '.ljust(8)
			rep_row += '|\n'
			rep += rep_row + breaker[i%2]
		rep += ' \t     '
		rep += ' '.join([l.ljust(9) for l in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']])
		return rep


		
class Space:
	def __init__(self, x, y, colour):
		assert colour in ['black', 'white'], 'Invalid colour for Space object'
		self.colour = colour
		self.x, self.y = x, y
		self.x_name, self.y_name = xy_to_board(x, y)
		self.held_by = None

	def occupy(self, Piece):
		self.held_by = Piece

	def vacate(self):
		self.held_by = None

	def get_Piece(self):
		return self.held_by

	def __str__(self):
		return 'Space '+ str(self.x_name) + str(self.y_name) + ' ('+self.colour+')'




class Game:
	def __init__(self):
		self.board = Board()
		self.board.setup_Game()
		self.all_piece_types = ('pawn', 'bishop', 'rook', 'knight', 'king', 'queen')
		self.all_colours = ('black', 'white')

def xy_to_board(x, y):
	return (['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'][x], y+1)

"""
import chess_game as cg
g = cg.Game()
print(g.board)
"""