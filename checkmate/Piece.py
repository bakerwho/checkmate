import checkmate as cm

class Piece:
	def __init__(self, piece_type, piece_colour, piece_name, xy):
		assert piece_colour.lower() in ['black', 'white'], 'Invalid colour'
		assert piece_type.lower() in ['pawn', 'bishop', 'rook', 'knight', 'king', 'queen'], 'Invalid piece_type'
		self.type = piece_type
		self.colour = piece_colour
		self.name = piece_name
		xy = cm.parse_xy(xy)
		self.xy = xy
		self.open_to_passant = False
		self.peace_moves = None
		self.kill_moves = None
		self.history = [xy]

	def set_xy(self, new_xy):
		new_xy = cm.parse_xy(new_xy)
		if new_xy is None:
			print('cannot set_xy for piece', self)
			return 0
		if self.type == 'pawn':
			if self.colour == 'white' and self.history[-1] == 1 and new_xy[0] == 3:
				self.open_to_passant = True
			elif self.colour == 'black' and self.history[-1] == 6 and new_xy[0] == 4:
				self.open_to_passant = True
		else:
			self.open_to_passant = False
		self.xy = new_xy
		self.history.append(new_xy)

	def update_Moves(self, Board):
		x, y = self.xy
		print('updating moves for', self.name)
		peace_moves, kill_moves = [], []
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
			for func in get_move_functions(self.type):
				i = 1
				new_xy = func((x, y, i))
				#print('\tchecking Space', cm.xy_to_board(new_xy))
				while Board.is_peace_Space(new_xy):
					#print('\tfound peace_move')
					peace_moves += [new_xy]
					i += 1
					new_xy = func((x, y, i))
				vals = Board.is_kill_Move(new_xy, current_xy = self.xy)
				if vals[0]:
					#print('\tfound kill_move')
					kill_moves.append(vals)
				#else:
					#print('\tnot a valid move')
		self.peace_moves = peace_moves
		self.kill_moves = kill_moves
		print('\t... finished')
		return peace_moves, kill_moves

	def get_xy(self):
		return self.xy
		
	def get_peace_Moves(self, board_coords = True):
		if board_coords:
			return cm.xy_to_board(self.peace_moves)
		else:
			return self.peace_moves

	def get_kill_Moves(self, board_coords = True):
		if board_coords:
			return cm.xy_to_board(self.kill_moves)
		else:
			return self.kill_moves

	def __str__(self):
		rep = 'Piece(' + str(self.name) + ') at ' + cm.xy_to_board(self.xy)
		return rep

	def __repr__(self):
		return self.__str__()

def get_move_functions(piece_type):
	assert piece_type in ['bishop', 'rook', 'queen'], str(piece_type)+' has no move functions'
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
	return funcs[piece_type]