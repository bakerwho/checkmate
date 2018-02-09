from __future__ import absolute_import

import sys

from checkmate.Piece import *
from checkmate.Space import *
from checkmate.Board import *
from checkmate.Game import *


from checkmate.utils import *
"""
import checkmate as cm
g = cm.Game()
print(g.gameboard)
b = g.gameboard
b.update_all_Moves()

b.move_Piece('b2', 'b4')
b.move_Piece('b4', 'b5')
b.move_Piece('c7', 'c5')
b
b.update_all_Moves()

p = b.get_Space('b2').get_Piece()

b.move_Piece('b2', 'b4')
b.get_Space('b1').vacate()
b.get_Space('a3').occupy(p)

pname = 'white_bishop0'
p = b.get_Piece('white_bishop0')
move_fs = cm.get_move_functions(wb.type)
"""