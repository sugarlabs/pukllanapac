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

from random import uniform
from sprites import Sprite
from card import Card, load_image

#
# Class for defining 3x3 matrix of cards
#
class Grid:
    """
    Grid positions correspond to one of:
    012  01x  012  01x
    345  34x  345  34x
    678  xxx  xxx  67x
    """
    def __init__(self, tw):
        self.grid = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        self.card_table = []
        self.mask_table = []
        # Stuff to keep around for the graphics
        self.w = int(tw.width)
        self.h = int(tw.height)
        self.d = int(tw.card_dim*tw.scale)
        self.s = tw.scale
        # Initialize the cards
        i = 0 # i is used as a label on the sprite
        for c in self.grid:
            x, y = self.i_to_xy(i)
            self.card_table.append(Card(tw,c,i,x,y))
            i += 1

    # Utility functions
    def i_to_xy(self, i):
        return int((self.w-(self.d*6))/2) + (i%6)*self.d - 10 + i%6*4,\
               int((self.h-(self.d*4))/2) + int(i/6)*self.d - 6 + int(i/6)*4

    def xy_to_i(self, x, y):
        return (x-int((self.w-(self.d*6))/2))/self.d +\
               ((y-int((self.h-(self.d*4))/2))/self.d)*6

    def set_grid(self, newgrid):
        for i, c in enumerate(newgrid):
            x, y = self.i_to_xy(i)
            self.card_table[c].spr.move((x,y))
            self.grid[i] = c

    def show_all(self):
        for i in range(9):
            self.card_table[i].spr.set_layer(100)

    def hide_list(self, list):
        for i in list:
            self.card_table[i].spr.hide()

    def hide_masks(self):
        for i in self.mask_table:
            i.hide()

    # Reset everything to initial layout
    def reset(self, tw):
        self.show_all()
        self.set_grid = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        self.test()

    # swap card a and card b
    # swap their entries in the grid and the position of their sprites
    def swap(self, a, b):
        # swap grid elements and x,y positions of sprites
        ai = self.grid.index(a)
        bi = self.grid.index(b)
        self.grid[bi] = a
        self.grid[ai] = b
        ax,ay = self.card_table[a].spr.get_xy()
        bx,by = self.card_table[b].spr.get_xy()
        self.card_table[a].spr.move((bx,by))
        self.card_table[b].spr.move((ax,ay))

    # print the grid
    def print_grid(self):
        print self.grid[0:3]
        print self.grid[3:6]
        print self.grid[6:9]
        return

    # Test all relevant borders, ignoring edges
    def test(self):
        return False
