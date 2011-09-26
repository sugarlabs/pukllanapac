#Copyright (c) 2010 Walter Bender

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public
# License along with this library; if not, write to the
# Free Software Foundation, 51 Franklin Street, Suite 500 Boston, MA
# 02110-1335 USA

import pygtk
pygtk.require('2.0')
import gtk
import gobject

from sprites import Sprite
from card import Card

HEX_TO_GRID = [-1, 0, 1, -1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
               17, 18, 19, 20, 21, 22, -1, 23, 24, -1]
GRID_TO_HEX = [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
               20, 21, 22, 23, 25, 26]
HEX_ORIENTATION = [-1, 180, 0, -1, 180, 0, 180, 0, 0, 180, 0, 180, 180, 0, 180,
                    0, 0, 180, 0, 180, 180, 0, 180, 0, -1, 180, 0, -1]
HEX2_TO_GRID = [-1, 0, 1, 2, 3, -1, 4, 5, 6, 7, 8, -1, 9, 10, 11, 12, 13, 14,
                 15, 16, 17, 18, 19, -1, -1, 20, 21, 22, 23, -1]
GRID_TO_HEX2 = [1, 2, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                21, 22, 25, 26, 27, 28]

class Grid:
    """ Class for defining matrix of cards """

    def __init__(self, tw, shape='rectangle'):
        """ Set initial grid positions: either a rectangle or a hexgaon """
        self.grid = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                     17, 18, 19, 20, 21, 22, 23]
        # Stuff to keep around for the graphics
        self.w = int(tw.width)
        self.h = int(tw.height)
        self.d = int(tw.card_dim * tw.scale)
        self.dx = self.d * 0.85
        self.dy = self.d * 0.5
        self.dy2 = self.d * 0.75
        self.s = tw.scale
        self.initialize_cards(tw.sprites, tw.path, tw.card_dim, tw.scale, shape)

    def initialize_cards(self, sprites, path, card_dim, scale, shape):
        if hasattr(self, 'card_table'):
            for c in self.card_table:
                c.spr.hide()
        self.card_table = []
        for i in self.grid:
            x, y = self.i_to_xy(i, shape)
            if shape == 'hexagon':
                self.card_table.append(Card(sprites, path, card_dim, scale, i,
                                            x, y, 'triangle'))
                self.card_table[i].set_orientation(
                    HEX_ORIENTATION[GRID_TO_HEX[i]])
            elif shape == 'hexagon2':
                self.card_table.append(Card(sprites, path, card_dim, scale, i,
                                            x, y, 'hexagon'))
            else:
                self.card_table.append(Card(sprites, path, card_dim, scale, i,
                                            x, y))

    def i_to_xy(self, i, shape='rectangle'):
        """ Convert a grid index to an x, y position """
        if shape == 'hexagon': # 4 x 7 with empty corners
            return int((self.w - (self.dx * 4)) / 2) + \
                (GRID_TO_HEX[i] % 4) * self.dx, \
                int((self.h - (self.dy * 7)) / 2) + \
                int(GRID_TO_HEX[i] / 4) * self.dy
        elif shape == 'hexagon2': # 6 x 5 with empty corners
            if int(GRID_TO_HEX2[i]/6) == 1 or \
               int(GRID_TO_HEX2[i]/6) == 3:
                hoffset = self.dx / 2
            else:
                hoffset = 0
            return int((self.w - (self.dx * 6)) / 2) + \
                (GRID_TO_HEX2[i] % 6) * self.dx + hoffset, \
                int((self.h - (self.dy2 * 5)) / 2) + \
                int(GRID_TO_HEX2[i] / 6) * self.dy2
        else: # 6 x 4
            return int((self.w - (self.d * 6)) / 2) + \
                (i % 6) * self.d - 10 + i % 6 * 4, \
                int((self.h - (self.d * 4)) / 2) + \
                int( i / 6) * self.d - 6 + int(i / 6) * 4

    def restore_grid(self, grid, shape='rectangle'):
        """ Move cards to x, y positions specified in grid """
        for i, c in enumerate(grid):
            x, y = self.i_to_xy(i, shape)
            self.card_table[c].spr.move((x, y))
            self.grid[i] = c

    def show_all(self):
        """ Make sure all of the cards are visible """
        for i in range(24):
            self.card_table[i].spr.set_layer(100)

    def hide_list(self, list):
        """ Hide the cards in the list """
        for i in list:
            self.card_table[i].spr.hide()

    def reset(self, shape='rectangle'):
        """ Reset everything to initial layout """
        self.show_all()
        self.grid = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                     17, 18, 19, 20, 21, 22, 23]
        for i in self.grid:
            x, y = self.i_to_xy(i, shape)
            self.card_table[i].spr.move((x, y))
            if shape == 'hexagon':
                self.card_table[i].set_orientation(
                    HEX_ORIENTATION[GRID_TO_HEX[i]])
            else:
                self.card_table[i].set_orientation(0)

    def swap(self, a, b, shape='rectangle'):
        """ swap grid elements and x,y positions of sprites """
        ai = self.spr_to_i(a)
        bi = self.spr_to_i(b)
        if ai == None or bi == None:
            return
        tmp = self.grid[bi]
        self.grid[bi] = self.grid[ai]
        self.grid[ai] = tmp
        ax, ay = a.get_xy()
        bx, by = b.get_xy()
        a.move((bx, by))
        b.move((ax, ay))
        if shape == 'hexagon':
            if HEX_ORIENTATION[GRID_TO_HEX[ai]] != \
                    HEX_ORIENTATION[GRID_TO_HEX[bi]]:
                print 'rotating 180: ', ai, bi, self.grid[ai], self.grid[bi]
                self.card_table[self.grid[ai]].rotate_180()
                self.card_table[self.grid[bi]].rotate_180()

    def spr_to_i(self, spr):
        """ Find a card index from a sprite """
        for i in range(24):
            if self.card_table[i].spr == spr:
                return self.card_to_i(i)
        return None

    def card_to_i(self, c):
        """ Find a grid index from a card """
        for i in range(24):
            if self.grid[i] == c:
                return i
