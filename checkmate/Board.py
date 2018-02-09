import checkmate as cm

class Board:
	def __init__(self, to_setup = False):
		colours = ('black', 'white')
		self.board = {i : { j : cm.Space((i, j), colours[(i+j)%2]) for j in range(8)} for i in range(8)}
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
		print('getting space', xy)
		x, y = cm.parse_xy(xy, True)
		return self.board[x][y]

	def get_Piece(self, piece_name):
		self.check_live_Pieces(correct = True)
		if piece_name in self.live_Pieces.keys():
			xy = self.live_Pieces[piece_name]
			return self.get_Space(xy).get_Piece()
		
	def add_Piece(self, xy, piece_type, piece_colour):
		xy = cm.parse_xy(xy)
		assert xy is not None, 'Invalid xy'
		assert self.xy_is_empty(xy), 'Space not empty'
		i = 0
		piece_name = piece_colour + '_' + piece_type + str(i)
		self.check_live_Pieces(correct = True)
		while piece_name in self.live_Pieces.keys() or piece_name in self.dead_Pieces.keys():
			i += 1
			piece_name = piece_name[:-1] + str(i)
		new_Piece = cm.Piece(piece_type, piece_colour, piece_name, xy)
		self.get_Space(xy).occupy(new_Piece)
		self.live_Pieces[piece_name] = xy

	def clear_Space(self, xy, dead = True):
		xy = cm.parse_xy(xy)
		self.check_live_Pieces(correct = True)
		piece = self.get_Space(xy).get_Piece()
		self.get_Space(xy).vacate()
		if dead:
			self.dead_Pieces[piece.name] = xy
			del self.live_Pieces[piece.name]

	def get_live_Pieces(self, update = False):
		all_Pieces = {}
		for row in self.board.values():
			for space in row.values():
				piece = space.get_Piece()
				if piece is not None:
					#print(type(piece), space)
					i = 0
					piece_name = piece.name	
					all_Pieces[piece_name] = space.xy
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

	def xy_is_empty(self, xy):
		self.check_live_Pieces(correct = True)
		return xy not in self.live_Pieces.values()

	def is_peace_Space(self, xy):
		xy = cm.parse_xy(xy)
		if xy is None:
			#print('Destination xy is not on board')
			return False
		return self.xy_is_empty(xy) 

	def is_kill_Move(self, xy, current_xy, is_pawn = False):
		xy = cm.parse_xy(xy)
		current_xy = cm.parse_xy(current_xy)
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
					if (	opp_Piece2 is not None and 
							opp_Piece2.type == 'pawn' and 
							opp_Piece2.open_to_passant and 
							opp_Piece2.colour == 'black'	):
						return xy, (x-1, y)
				elif current_Piece.colour == 'black' and current_xy[0] == 3:
					opp_Piece2 = self.board[x+1][y].get_Piece()
					if (	opp_Piece2 is not None and 
							opp_Piece2.type == 'pawn' and 
							opp_Piece2.open_to_passant  and 
							opp_Piece2.colour == 'white'	):
						return xy, (x+1, y)
				else:
					return False, None
			else:
				if opp_Piece.colour == current_Piece.colour:
					return False, None
				else:
					return xy, xy
			return False, None

	def update_all_Moves(self):
		self.check_live_Pieces(correct = True)
		self.all_Moves = {'white': {}, 'black': {}}
		for piece_name, xy in self.live_Pieces.items():
			#print('checking moves for', piece_name, xy)
			kill_Moves, peace_Moves = self.get_Space(xy).get_Piece().update_Moves(self)
			self.all_Moves[piece_name[:5]][piece_name] = {'kill_Moves' : kill_Moves, 'peace_Moves' : peace_Moves}

	def get_Space(self, xy):
		x, y = cm.parse_xy(xy, True)
		return self.board[x][y]

	def move_Piece(self, xy_1, xy_2):
		p1 = self.get_Space(xy_1).get_Piece()
		assert p1 is not None, 'No piece on given Space'
		p2 = self.get_Space(xy_2).get_Piece()
		if p2 is not None:
			print('killing piece', p2)
		p1.set_xy(xy_2)
		self.get_Space(xy_1).vacate()
		self.get_Space(xy_2).occupy(p1)
		self.live_Pieces[p.name] = xy_2
		self.check_live_Pieces(correct = True)


	def clear_Board(self):
		self.__init__()

	def __str__(self):
		rep = '\t ' + '_'*87+ '\n'
		breaker =  ['\t|'+''.join(['          |**********|' for i in range(4)]) + '\n' + 
					'\t|'+''.join(['__________|__________|' for i in range(4)]) + '\n', 
					'\t|'+''.join(['**********|          |' for i in range(4)]) + '\n' + 
					'\t|'+''.join(['__________|__________|' for i in range(4)]) + '\n']
		for i in range(len(self.board), 0, -1):
			row = self.board[i-1]
			rep_row = str(i) + '\t'
			for j in range(len(row)):
				space = row[j]
				if space.held_by is not None:
					rep_row += '| '+str(space.held_by.name[0]+space.held_by.name[5:]).ljust(9)
				else:
					rep_row += '| '+' '.ljust(9)
			rep_row += '|\n'
			rep += rep_row + breaker[i%2]
		rep += ' \t     '
		rep += ' '.join([l.ljust(10) for l in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']])
		return rep

	def __repr__(self):
		return self.__str__()


		



