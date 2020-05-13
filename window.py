#Copyright (c) 2010,11 Walter Bender

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public
# License along with this library; if not, write to the
# Free Software Foundation, 51 Franklin Street, Suite 500 Boston, MA
# 02110-1335 USA

from gi.repository import Gtk
from gi.repository import Gdk
import gobject
from math import sqrt

from gettext import gettext as _

try:
    from sugar3.graphics import style
    GRID_CELL_SIZE = style.GRID_CELL_SIZE
except:
    GRID_CELL_SIZE = 0

from grid import Grid
from sprites import Sprites
from constants import C, MASKS, CARD_DIM

import logging
_logger = logging.getLogger('pukllanapac-activity')

LEVEL_BOUNDS = [[[1, 2], [0, 1], [2, 3], [1, 2]],
                [[1, 2], [0, 1], [1, 4], [0, 3]], 
                [[0, 3], [-1, 2], [1, 5], [-1, 4]]]


class Game():
    """ The game play -- called from within Sugar or GNOME """

    def __init__(self, canvas, path, parent=None):
        """ Initialize the playing surface """

        self.path = path
        self.activity = parent

        # starting from command line
        # we have to do all the work that was done in CardSortActivity.py
        if parent is None:
            self.sugar = False
            self.canvas = canvas

        # starting from Sugar
        else:
            self.sugar = True
            self.canvas = canvas
            parent.show_all()

            self.canvas.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
            self.canvas.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK)
            self.canvas.connect("draw", self._draw_cb)
            self.canvas.connect("button-press-event", self._button_press_cb)
            self.canvas.connect("button-release-event", self._button_release_cb)
            self.canvas.connect("key_press_event", self._keypress_cb)
            self.width = Gdk.Screen.width()
            self.height = Gdk.Screen.height() - GRID_CELL_SIZE
            self.card_dim = CARD_DIM
            self.scale = 0.6 * self.height / (self.card_dim * 3)

        # Initialize the sprite repository
        self.sprites = Sprites(self.canvas)

        # Initialize the grid
        self.mode = 'rectangle'
        self.grid = Grid(self, self.mode)
        self.bounds = LEVEL_BOUNDS[0]
        self.level = 0

        # Start solving the puzzle
        self.press = None
        self.release = None
        self.start_drag = [0, 0]

    def _button_press_cb(self, win, event):
        win.grab_focus()
        x, y = list(map(int, event.get_coords()))
        self.start_drag = [x, y]
        spr = self.sprites.find_sprite((x, y))
        if spr is None:
            self.press = None
            self.release = None
            return True
        # take note of card under button press
        self.press = spr
        return True

    def _button_release_cb(self, win, event):
        win.grab_focus()
        x, y = list(map(int, event.get_coords()))
        spr = self.sprites.find_sprite((x, y))
        if spr is None:
            self.press = None
            self.release = None
            return True
        # take note of card under button release
        self.release = spr
        # if press and release are the same card (click), then rotate
        if self.press == self.release:
            self.press.set_layer(0)
            self.grid.card_table[self.grid.grid[self.grid.spr_to_i(
                        self.press)]].rotate_ccw()
            if self.mode == 'hexagon': # Rotate a second time
                self.grid.card_table[self.grid.grid[self.grid.spr_to_i(
                            self.press)]].rotate_ccw()
            self.press.set_layer(100)
        else:
            self.grid.swap(self.press, self.release, self.mode)            
        self.press = None
        self.release = None
        if self.test() == True:
            if self.level < 2:
                gobject.timeout_add(3000, self.activity.change_play_level_cb,
                                    None)
        return True

    def _keypress_cb(self, area, event):
        """ Keypress is used to ...  """
        k = Gdk.keyval_name(event.keyval)

    def _expose_cb(self, win, event):
        ''' Callback to handle window expose events '''
        self.do_expose_event(event)
        return True

    def _draw_cb(self, canvas, cr):
        self.sprites.redraw_sprites(cr=cr)

    def do_expose_event(self, event):
        ''' Handle the expose-event by drawing '''
        # Restrict Cairo to the exposed area
        cr = self.canvas.props.window.cairo_create()
        cr.rectangle(event.area.x, event.area.y,
                event.area.width, event.area.height)
        cr.clip()
        # Refresh sprite list
        self.sprites.redraw_sprites(cr=cr)

    def _destroy_cb(self, win, event):
        Gtk.main_quit()

    def mask(self, level):
        """ mask out cards not on play level """
        self.grid.hide_list(MASKS[level])
        self.bounds = LEVEL_BOUNDS[level]
        self.level = level

    def test(self):
        """ Test the grid to see if the level is solved """
        if self.mode != 'rectangle':
            return False
        for i in range(24):
            if i not in MASKS[self.level]:
                if not self.test_card(i):
                    return False
        return True

    def test_card(self, i):
        """ Test a card with its neighbors; tests are bounded by the level """
        row = int(i/6)
        col = i%6
        if row > self.bounds[0][0] and row <= self.bounds[0][1]:
            if C[self.grid.grid[i]][rotate_index(0,
                 self.grid.card_table[self.grid.grid[i]].orientation)] != \
               C[self.grid.grid[i - 6]][rotate_index(1,
                 self.grid.card_table[self.grid.grid[i - 6]].orientation)]:
                return False
            if C[self.grid.grid[i]][rotate_index(3,
                 self.grid.card_table[self.grid.grid[i]].orientation)] != \
               C[self.grid.grid[i - 6]][rotate_index(2,
                 self.grid.card_table[self.grid.grid[i - 6]].orientation)]:
                return False
        if col > self.bounds[2][0] and col <= self.bounds[2][1]:
            if C[self.grid.grid[i]][rotate_index(3,
                 self.grid.card_table[self.grid.grid[i]].orientation)] != \
               C[self.grid.grid[i - 1]][rotate_index(0,
                 self.grid.card_table[self.grid.grid[i - 1]].orientation)]:
                return False
            if C[self.grid.grid[i]][rotate_index(2,
                 self.grid.card_table[self.grid.grid[i]].orientation)] != \
               C[self.grid.grid[i - 1]][rotate_index(1,
                 self.grid.card_table[self.grid.grid[i - 1]].orientation)]:
                return False
        return True

def rotate_index(index, orientation):
    """ Account for orientation when computing an index """
    return (index + int(orientation/90)) % 4

def distance(start, stop):
    """ Measure the length of drag between button press and button release. """
    dx = start[0] - stop[0]
    dy = start[1] - stop[1]
    return sqrt(dx * dx + dy * dy)
