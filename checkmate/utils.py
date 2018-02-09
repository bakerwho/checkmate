import checkmate as cm

def xy_to_board(xy):
	if type(xy) == tuple and len(xy) == 2:
		if xy_on_board(xy):
			x, y = xy
			return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'][y] + str(x+1)
	elif type(xy) == list:
		return [xy_to_board(xy0) for xy0 in xy]
	return None

def xy_on_board(xy):
	if type(xy) == tuple and len(xy) == 2:
		a = xy[0] in range(8) and xy[1] in range(8)
		return a
	else:
		return 'xy not on board'

def parse_xy(xy, report_error = False):
	if type(xy) == tuple and len(xy) == 2:
		if xy_on_board(xy):
			return xy
		else:
			return None
	elif type(xy) == str and len(xy) == 2:
		y, x = xy[0], int(xy[1])
		if y in 'abcdefgh' and x in range(1, 9):
			y, x = dict(zip('abcdefgh', range(8)))[y], x-1
			return (x, y)
		else:
			return None
	if report_error:
		print('invalid xy:', xy)
	return None 