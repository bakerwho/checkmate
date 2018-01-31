class Piece:
	def __init__(self, piece_type, piece_colour, piece_name, xy = None):
		assert piece_colour.lower() in ['black', 'white'], 'Invalid colour'
		assert piece_type.lower() in ['pawn', 'bishop', 'rook', 'knight', 'king', 'queen'], 'Invalid piece_type'
		self.type = piece_type
		self.colour = piece_colour
		self.name = piece_name
		if xy is None:
			print('Warning : xy initialised as None')
		else:
			assert xy[0] in range(8) and xy[1] in range(8), 'Piece location out of range'
		self.xy = xy
		self.open_to_passant = False
		self.peace_moves = None
		self.kill_moves = None

	def set_xy(self, xy):
		assert x in range(8) and y in range(8), 'Piece location out of range'
		if self.type == 'pawn':
			if self.colour == 'white' and self.xy[0] == 1 and xy[0] == 3:
				self.open_to_passant = True
			elif self.colour == 'black' and self.xy[0] == 6 and xy[0] == 4:
				self.open_to_passant = True
		else:
			self.open_to_passant = False
		self.xy = xy

		def get_all_Moves(self, Board):
		x, y = self.xy
		peace_moves, kill_moves = [], []
		move_functions_dict = get_move_functions(self.type)
		if self.type == 'pawn':
			if self.colour == 'white':
				peace_moves.append((x + 1, y))
				kill_moves += [(x + 1, y + 1), (x + 1, y - 1)]
				if x == 1:
					peace_moves.append((x + 2, y))
			else:
				peace_moves.append((x - 1, y))
				kill_moves += [(x - 1, y + 1), (x - 1, y - 1)]
				if x == 6:
					peace_moves.append((x - 2, y))
			peace_moves = [xy for xy in peace_moves if Board.is_peace_Move(xy)]
			kill_moves = [Board.is_kill_Move(new_xy, current_xy = self.xy, is_pawn = True) for new_xy in kill_moves]
			kill_moves = [val for val in kill_moves if val[0]]
		elif self.type == 'knight':
			peace_moves = [xy for xy in list(zip(	[x+2, x+2, x+1 , x+1, x-1, x-1, x-2, x-2], 
								 					[y+1, y-1, y+2, y-2, y+2, y-2, y+1, y-1]))
									if Board.is_peace_Move(xy)]
			kill_moves = list(zip(	[x+2, x+2, x+1 , x+1, x-1, x-1, x-2, x-2], 
								 				[y+1, y-1, y+2, y-2, y+2, y-2, y+1, y-1]))
			kill_moves = [Board.is_kill_Move(new_xy, current_xy = self.xy, is_pawn = True) for new_xy in kill_moves]
			kill_moves = [val for val in kill_moves if val[0]]
		elif self.type == 'king':
			peace_moves = [xy for xy in list(zip(	[x  , x  , x+1, x+1, x+1, x-1, x-1, x-1], 
								 				[y+1, y-1, y  , y+1, y-1, y  , y+1, y-1]))
									if Board.is_peace_Move(xy)]
			kill_moves = list(zip(	[x  , x  , x+1, x+1, x+1, x-1, x-1, x-1], 
								 	[y+1, y-1, y  , y+1, y-1, y  , y+1, y-1]))
			kill_moves = [Board.is_kill_Move(new_xy, current_xy = self.xy, is_pawn = True) for new_xy in kill_moves]
			kill_moves = [val for val in kill_moves if val[0]]
		elif self.type in ['bishop', 'queen', 'rook']:
			for func in move_functions_dict[self.type]:
				i = 1
				new_xy = func((x, y, i))
				while Board.is_peace_Move(new_xy) or Board.is_kill_Move(new_xy, current_xy = self.xy)[0]:
					vals = Board.is_kill_Move(new_xy, current_xy = self.xy)
					if vals[0]:
						kill_moves.append(vals)
						break
					peace_moves += [new_xy]
					i += 1
		self.peace_moves = peace_moves
		self.kill_moves = kill_moves
		return peace_moves+kill_moves

	def get_xy(self):
		return self.xy
		
	def get_peace_Moves(self):
		return self.peace_moves

	def get_kill_Moves(self):
		return self.kill_moves



	def __str__(self):
		rep = 'Piece(' + str(self.type) + ', ' + str(self.colour) + ')' #at '+self.get_Space().__str__()
		return rep

class Board:
	def __init__(self, to_setup = False):
		colours = ('black', 'white')
		self.board = [[Space(i, j, colours[(i+j)%2]) for i in range(8)] for j in range(8)]
		self.occupied_spaces = []
		self.live_Pieces = {}
		self.dead_Pieces = {}
		if to_setup:
			self.setup_Game()

	def setup_Game(self):
		colours = ('white', 'black')
		pieces = ('rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook')
		for colour_no in range(len(colours)):
			colour = colours[colour_no]
			for y in range(8):
				x = colour_no * 5 + 1
				self.add_Piece('pawn', colour, (x, y))
			for y in range(len(pieces)):
				x = colour_no*7
				self.add_Piece(pieces[y], colour, (x, y))
		self.update_live_Pieces()
	
	def add_Piece(self, piece_type, piece_colour, xy):
		assert self.Space_is_on_board(xy), 'Space not on board'
		assert self.Space_is_empty(xy), 'Space not empty'
		self.update_live_Pieces()
		i = 0
		piece_name = piece_colour + '_' + piece_type + str(i)
		while piece_name in self.live_Pieces.keys():
			i += 1
			piece_name = piece_name[:-1] + str(i)
		new_Piece = Piece(piece_type, piece_colour, piece_name, xy)
		self.occupied_spaces.append(xy)
		self.board[xy[0]][xy[1]].occupy(new_Piece)

	def clear_Space(self, xy):
		x, y = xy
		piece = self.board[x][y].get_Piece()
		self.board[x][y].vacate()
		self.dead_Pieces[piece.name] = piece
		self.occupied_spaces.remove(xy)
		self.update_live_Pieces()


	def update_live_Pieces(self):
		all_Pieces = {}
		for row in self.board:
			for Space in row:
				Piece = Space.get_Piece()
				if Piece is not None:
					#print(type(Piece), Space)
					i = 0
					piece_name = Piece.colour + ' ' + Piece.type + str(i)
					#print(all_Pieces.keys(), piece_name)
					while piece_name in all_Pieces.keys():
						i = i + 1
						piece_name = piece_name[:-1] + str(i)	
					all_Pieces[piece_name] = Piece
		self.live_Pieces = all_Pieces

	def Space_is_on_board(self, xy):
		return xy[0] in range(8) and xy[1] in range(8)

	def Space_is_empty(self, xy):
		return xy not in self.occupied_spaces

	def is_peace_Move(self, xy):
		return self.Space_is_on_board(xy) and self.Space_is_empty(xy)

	def is_kill_Move(self, xy, current_xy, is_pawn = False):
		assert current_xy is not None, 'Specify current xy'
		if not self.Space_is_on_board(xy):
			#print('Destination xy is not on board')
			return False, None
		assert self.Space_is_on_board(current_xy), 'Current xy is not on board'
		current_colour = self.board[current_xy[0]][current_xy[1]].get_Piece().colour
		x, y = xy
		if not is_pawn:
			opp_Piece = self.board[x][y].get_Piece()
			if opp_Piece is None:
				#print('No Piece at ' + str(xy))
				return False, None
			else:
				if opp_Piece.colour == current_colour:
					return False, None
				else:
					return xy, xy
		else:
			opp_Piece = self.board[x][y].get_Piece()
			if opp_Piece is None:
				if current_colour == 'white' and current_xy[0] == 4:
					opp_Piece2 = self.board[x-1][y].get_Piece()
					if opp_Piece2.type == 'pawn' and opp_Piece2.open_to_passant and opp_Piece2.colour == 'black':
						return xy, (x-1, y)
				elif current_colour == 'black' and current_xy[0] == 3:
					opp_Piece2 = self.board[x+1][y].get_Piece()
					if opp_Piece2.type == 'pawn' and opp_Piece2.open_to_passant  and opp_Piece2.colour == 'white':
						return xy, (x+1, y)
				else:
					return False, None
			else:
				if opp_Piece.colour == current_colour:
					return False, None
				else:
					return xy, xy

	def update_moves(self, piece_name):
		for row in self.board:
			for Space in row:



	def get_Space(self, xy):
		return self.board[x][y]

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
		self.gameboard = Board()
		self.gameboard.setup_Game()
		self.all_piece_types = ('pawn', 'bishop', 'rook', 'knight', 'king', 'queen')
		self.all_colours = ('black', 'white')


def get_move_functions(piece_type):
	bishfuncs = [	lambda xyi : (xyi[0] + xyi[2], xyi[1] + xyi[2]), 
					lambda xyi : (xyi[0] + xyi[2], xyi[1] - xyi[2]),
					lambda xyi : (xyi[0] - xyi[2], xyi[1] + xyi[2]),
					lambda xyi : (xyi[0] - xyi[2], xyi[1] - xyi[2])]
	rookfuncs = [	lambda xyi : (xyi[0] + xyi[2], xyi[1]), 
					lambda xyi : (xyi[0] - xyi[2], xyi[1]),
					lambda xyi : (xyi[0]         , xyi[1] + xyi[2]),
					lambda xyi : (xyi[0]         , xyi[1] - xyi[2])]
	queenfuncs = bishfuncs + rookfuncs
	funcs = dict(zip(['bishop', 'rook', 'queen'], [bishfuncs, rookfuncs, queenfuncs]))
	return funcs

def xy_to_board(x, y):
	return (['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'][x], y+1)

"""
import chess_game as cg
g = cg.Game()
print(g.gameboard)
g.gameboard.board[0][0]
g.gameboard.board[0][0].get_Piece().name
g.gameboard.board[0][0].get_Piece().get_all_Moves(g.gameboard)
"""