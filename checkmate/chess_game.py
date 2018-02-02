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
			xy = parse_xy(xy)
			assert xy[0] in range(8) and xy[1] in range(8), 'Piece location out of range'
		self.xy = xy
		self.open_to_passant = False
		self.peace_moves = None
		self.kill_moves = None

	def set_xy(self, xy):
		xy = parse_xy(xy)
		assert x in range(8) and y in range(8), 'Piece location out of range'
		if self.type == 'pawn':
			if self.colour == 'white' and self.xy[0] == 1 and xy[0] == 3:
				self.open_to_passant = True
			elif self.colour == 'black' and self.xy[0] == 6 and xy[0] == 4:
				self.open_to_passant = True
		else:
			self.open_to_passant = False
		self.xy = xy

	def update_Moves(self, Board):
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
			peace_moves = [xy for xy in peace_moves if Board.is_peace_Space(xy)]
			kill_moves = [Board.is_kill_Move(new_xy, current_xy = self.xy, is_pawn = True) for new_xy in kill_moves]
			kill_moves = [val for val in kill_moves if val[0]]
		elif self.type == 'knight':
			peace_moves = [xy for xy in list(zip(	[x+2, x+2, x+1 , x+1, x-1, x-1, x-2, x-2], 
								 					[y+1, y-1, y+2, y-2, y+2, y-2, y+1, y-1]))
									if Board.is_peace_Space(xy)]
			kill_moves = list(zip(	[x+2, x+2, x+1 , x+1, x-1, x-1, x-2, x-2], 
								 				[y+1, y-1, y+2, y-2, y+2, y-2, y+1, y-1]))
			kill_moves = [Board.is_kill_Move(new_xy, current_xy = self.xy, is_pawn = True) for new_xy in kill_moves]
			kill_moves = [val for val in kill_moves if val[0]]
		elif self.type == 'king':
			peace_moves = [xy for xy in list(zip(	[x  , x  , x+1, x+1, x+1, x-1, x-1, x-1], 
								 				[y+1, y-1, y  , y+1, y-1, y  , y+1, y-1]))
									if Board.is_peace_Space(xy)]
			kill_moves = list(zip(	[x  , x  , x+1, x+1, x+1, x-1, x-1, x-1], 
								 	[y+1, y-1, y  , y+1, y-1, y  , y+1, y-1]))
			kill_moves = [Board.is_kill_Move(new_xy, current_xy = self.xy, is_pawn = True) for new_xy in kill_moves]
			kill_moves = [val for val in kill_moves if val[0]]
		elif self.type in ['bishop', 'queen', 'rook']:
			for func in move_functions_dict[self.type]:
				i = 1
				new_xy = func((x, y, i))
				while Board.is_peace_Space(new_xy) or Board.is_kill_Move(new_xy, current_xy = self.xy)[0]:
					vals = Board.is_kill_Move(new_xy, current_xy = self.xy)
					if vals[0]:
						kill_moves.append(vals)
						break
					peace_moves += [new_xy]
					i += 1
		self.peace_moves = peace_moves
		self.kill_moves = kill_moves
		return peace_moves, kill_moves

	def get_xy(self):
		return self.xy
		
	def get_peace_Moves(self, board_coords = True):
		if board_coords:
			return xy_to_board(self.peace_moves)
		else:
			return self.peace_moves

	def get_kill_Moves(self, board_coords = True):
		if board_coords:
			return xy_to_board(self.kill_moves)
		else:
			return self.kill_moves

	def __str__(self):
		rep = 'Piece(' + str(self.name) + ') at ' + xy_to_board(self.xy)
		return rep

	def __repr__(self):
		return self.__str__()

class Board:
	def __init__(self, to_setup = False):
		colours = ('black', 'white')
		self.board = [[Space((i, j), colours[(i+j)%2]) for j in range(8)] for i in range(8)]
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
				self.add_Piece((x, y), 'pawn', colour)
			for y in range(len(pieces)):
				x = colour_no*7
				self.add_Piece((x, y), pieces[y], colour)
			self.check_live_Pieces(correct = True)

	def get_Space(self, xy):
		x, y = parse_xy(xy, True)
		return self.board[x][y]
		
	def add_Piece(self, xy, piece_type, piece_colour):
		xy = parse_xy(xy)
		assert xy is not None, 'Invalid xy'
		assert self.xy_is_empty(xy), 'Space not empty'
		i = 0
		piece_name = piece_colour + '_' + piece_type + str(i)
		self.check_live_Pieces(correct = True)
		while piece_name in self.live_Pieces.keys() or piece_name in self.dead_Pieces.keys():
			i += 1
			piece_name = piece_name[:-1] + str(i)
		new_Piece = Piece(piece_type, piece_colour, piece_name, xy)
		self.get_Space(xy).occupy(new_Piece)
		self.live_Pieces[piece_name] = xy

	def clear_Space(self, xy, dead = True):
		xy = parse_xy(xy)
		piece = self.get_Space(xy).get_Piece()
		self.get_Space(xy).vacate()
		if dead:
			self.dead_Pieces[piece.name] = xy
			del self.live_Pieces[piece.name]

	def get_live_Pieces(self, update = False):
		all_Pieces = {}
		for row in self.board:
			for Space in row:
				Piece = Space.get_Piece()
				if Piece is not None:
					#print(type(Piece), Space)
					i = 0
					piece_name = Piece.name	
					all_Pieces[piece_name] = Space.xy
		return all_Pieces

	def check_live_Pieces(self, correct = False):
		correct_live_Pieces = self.get_live_Pieces()
		if self.live_Pieces == correct_live_Pieces:
			return True
		else:
			#print("live_Pieces don't match")
			if correct:
				self.live_Pieces = correct_live_Pieces
				print('corrected live_Pieces')
			return False

	def xy_on_board(self, xy):
		return xy[0] in range(8) and xy[1] in range(8)

	def xy_is_empty(self, xy):
		return xy not in self.live_Pieces.values()

	def is_peace_Space(self, xy):
		xy = parse_xy(xy)
		if xy is None:
			#print('Destination xy is not on board')
			return False
		return self.xy_is_empty(xy) 

	def is_kill_Move(self, xy, current_xy, is_pawn = False):
		xy = parse_xy(xy)
		current_xy = parse_xy(current_xy)
		if xy is None:
			#print('Destination xy is not on board')
			return False, None
		if current_xy is None:
			print('Invalid current_xy. There may be an error.')
			return False, None
		current_Piece = self.get_Space(current_xy).get_Piece()
		if current_Piece is None:
			return False, None
		if not is_pawn:
			opp_Piece = self.get_Space(xy).get_Piece()
			if opp_Piece is None:
				#print('No Piece at ' + str(xy))
				return False, None
			else:
				if opp_Piece.colour == current_Piece.colour:
					return False, None
				else:
					return xy, xy
		else:			# if pawn
			opp_Piece = self.get_Space(xy).get_Piece()
			"""assert (	xy[0] == current_xy[0] + 1 and 
															current_Piece.colour == 'white') or (
															xy[0] == current_xy[0] - 1 and 
															current_Piece.colour == 'black')"""
			x, y = xy
			if opp_Piece is None:
				if current_Piece.colour == 'white' and current_xy[0] == 4:
					opp_Piece2 = self.board[x-1][y].get_Piece()
					if opp_Piece2.type == 'pawn' and opp_Piece2.open_to_passant and opp_Piece2.colour == 'black':
						return xy, (x-1, y)
				elif current_Piece.colour == 'black' and current_xy[0] == 3:
					opp_Piece2 = self.board[x+1][y].get_Piece()
					if opp_Piece2.type == 'pawn' and opp_Piece2.open_to_passant  and opp_Piece2.colour == 'white':
						return xy, (x+1, y)
				else:
					return False, None
			else:
				if opp_Piece.colour == current_Piece.colour:
					return False, None
				else:
					return xy, xy

	def update_all_Moves(self):
		self.check_live_Pieces(correct = True)
		for piece_name, xy in self.live_Pieces.items():
			print('checking moves for', piece_name)
			self.get_Space(xy).get_Piece().update_Moves(self)

	def get_Space(self, xy):
		x, y = parse_xy(xy)
		return self.board[x][y]

	def move_Piece(self, xy_1, xy_2):
		p = self.get_Space(xy_1).get_Piece()
		self.get_Space(xy_1).vacate()
		self.get_Space(xy_2).occupy(p)


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

	def __repr__(self):
		return self.__str__()


		
class Space:
	def __init__(self, xy, colour):
		assert colour in ['black', 'white'], 'Invalid colour for Space object'
		self.colour = colour
		x, y = xy
		self.x, self.y = x, y
		self.xy = (x, y)
		self.x_name, self.y_name = xy_to_board(xy)
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




class Game:
	def __init__(self):
		self.gameboard = Board()
		self.gameboard.setup_Game()
		self.all_piece_types = ('pawn', 'bishop', 'rook', 'knight', 'king', 'queen')
		self.all_colours = ('black', 'white')

	def __str__(self):
		return self.gameboard.__str__()

	def __repr__(self):
		return self.gameboard.__repr__()


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

def xy_to_board(xy):
	if type(xy) == tuple and len(xy) == 2:
		if xy < (8, 8) and (xy) >= (0, 0):
			x, y = xy
			return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'][y] + str(x+1)
	elif type(xy) == list:
		return [xy_to_board(xy0) for xy0 in xy]
	return None

def parse_xy(xy, report_error = False):
	if type(xy) == tuple and len(xy) == 2:
		if xy < (8, 8) and xy >= (0, 0):
			return xy
	elif type(xy) == str and len(xy) == 2:
		y, x = xy[0], int(xy[1])
		if y in 'abcdefgh' and x in range(1, 9):
			y, x = dict(zip('abcdefgh', range(8)))[y], x-1
			return (x, y)
	if report_error:
		print('invalid xy:', xy)
	return None 



"""
import checkmate as cm
g = cm.Game()
print(g.gameboard)
b = g.gameboard
b.update_all_Moves()

b.move_Piece('b2', 'b4')
b.move_Piece('b4', 'b5')
b.move_Piece('c7', 'c5')
b.update_all_Moves()

p = b.get_Space('b2').get_Piece()

b.move_Piece('b2', 'b4')
b.get_Space('b1').vacate()
b.get_Space('a3').occupy(p)


"""
