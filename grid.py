#Copyright (c) 2010 Walter Bender

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import pygtk
pygtk.require('2.0')
import gtk
import gobject

from sprites import Sprite
from card import Card, load_image


class Grid:
    """ Class for defining 6x4 matrix of cards """
    def __init__(self, tw):
        """ Grid positions """
        self.grid = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                     17, 18, 19, 20, 21, 22, 23]
        self.card_table = []
        # Stuff to keep around for the graphics
        self.w = int(tw.width)
        self.h = int(tw.height)
        self.d = int(tw.card_dim * tw.scale)
        self.s = tw.scale
        # Initialize the cards
        for i in self.grid:
            x, y = self.i_to_xy(i)
            self.card_table.append(Card(tw, i, x, y))

    def i_to_xy(self, i):
        """ Convert a grid index to an x, y position """
        return int((self.w - (self.d * 6)) / 2) + \
            (i % 6) * self.d - 10 + i % 6 * 4, \
            int((self.h - (self.d * 4)) / 2) + \
            int( i / 6) * self.d - 6 + int(i/6)*4

    def xy_to_i(self, x, y):
        """ Convert an x, y position to a grid index """
        return (x - int((self.w - (self.d * 6)) / 2)) / self.d + \
            ((y - int((self.h - (self.d * 4)) / 2)) / self.d) * 6

    def set_grid(self, newgrid):
        """ Move cards to x, y positions specified in grid """
        for i, c in enumerate(newgrid):
            x, y = self.i_to_xy(i)
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

    def reset(self):
        """ Reset everything to initial layout """
        self.show_all()
        self.grid = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                     17, 18, 19, 20, 21, 22, 23]
        for i in self.grid:
            x, y = self.i_to_xy(i)
            self.card_table[i].spr.move((x, y))

    def swap(self, a, b):
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
