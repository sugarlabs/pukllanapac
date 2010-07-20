#!/usr/bin/env python

#Copyright (c) 2009,10 Walter Bender

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

R = "#ff0000"
Y = "#ffff00"
B = "#0000ff"
G = "#00ff00"

C = [[Y, B, Y, R], [R, Y, Y, R], [R, R, Y, R], [R, R, R, R], [B, B, B, Y], [Y, B, Y, Y],
     [R, B, R, R], [Y, Y, Y, Y], [Y, Y, R, B], [Y, Y, B, B], [Y, R, Y, Y], [R, R, Y, B],
     [B, B, B, B], [R, B, B, B], [B, R, B, R], [B, B, R, R], [R, R, B, Y], [B, Y, B, Y],
     [R, Y, Y, B], [R, B, B, Y], [Y, R, B, R], [R, Y, R, Y], [R, B, Y, B], [Y, B, B, R]]

H = [[G, B, G], [B, Y, R], [B, R, B], [Y, G, Y], [R, G, B], [G, B, B], [R, B, G], [B, B, B], [R, R, R], [R, R, B], [G, R, R], [Y, R, R], [R, G, Y], [G, G, Y], [G, R, Y], [B, Y, G], [Y, R, Y], [G, G, R], [G, G, G], [B, Y, Y], [R, Y, B], [Y, B, G], [Y, Y, Y], [Y, B, B]]

RT = [[B, B, Y], [Y, B, G], [G, R, B], [Y, G, Y], [R, G, G], [Y, G, B], [B, G, G], [R, B, Y], [R, R, G], [R, Y, G], [B, B, R], [Y, Y, Y]]

LT = [[B, B, G], [R, Y, Y], [G, G, G], [G, Y, G], [G, R, B], [B, Y, Y], [B, B, B], [B, R, R], [Y, R, R], [R, R, R], [R, B, Y], [R, Y, G]]

MASKS = [[0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22,
          23], [0, 1, 2, 3, 4, 5, 6, 11, 12, 17, 18, 19, 20, 21, 22, 23], []]

CARD_DIM = 200

