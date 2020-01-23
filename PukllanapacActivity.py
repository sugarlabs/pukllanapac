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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

import sugar3
from sugar3.activity import activity
try:
    from sugar3.graphics.toolbarbox import ToolbarBox
    _have_toolbox = True
except ImportError:
    _have_toolbox = False

if _have_toolbox:
    from sugar3.bundle.activitybundle import ActivityBundle
    from sugar3.activity.widgets import ActivityToolbarButton
    from sugar3.activity.widgets import StopButton
    from sugar3.graphics.toolbarbox import ToolbarButton

from sugar3.datastore import datastore

from gettext import gettext as _
import locale
import os.path

from toolbar_utils import radio_factory, label_factory, separator_factory, \
    button_factory
from window import Game

SERVICE = 'org.sugarlabs.PukllanapacActivity'
IFACE = SERVICE
PATH = '/org/augarlabs/PukllanapacActivity'
LEVEL_ICONS = ['level1', 'level2', 'level3']
GAME_ICONS = ['rectangle', 'hexagon', 'hexagon2']


class PukllanapacActivity(activity.Activity):
    """ Sliding puzzle game """

    def __init__(self, handle):
        """ Initialize the toolbars and the game board """
        super(PukllanapacActivity,self).__init__(handle)

        self._play_level = 0
        self._play_mode = 0
        self._setup_toolbars(_have_toolbox)

        # Create a canvas
        canvas = Gtk.DrawingArea()
        canvas.set_size_request(Gdk.Screen.width(), \
                                Gdk.Screen.height())
        self.set_canvas(canvas)
        canvas.show()
        self.show_all()

        self.win = Game(canvas, os.path.join(activity.get_bundle_path(),
                                            'images'), self)

        # Restore game state from Journal or start new game
        if 'play_level' in self.metadata:
            self.change_play_level_cb(play_level=int(
                    self.metadata['play_level']))
        if 'play_mode' in self.metadata:
            self.change_play_mode_cb(play_mode=int(
                    self.metadata['play_mode']))
        grid = []
        for i in range(24):
            if 'card' + str(i) in self.metadata:
                grid.append(int(self.metadata['card' + str(i)]))
            self.win.grid.restore_grid(grid, self.win.mode)
        for i in range(24):
            if 'rotate' + str(i) in self.metadata:
                self.win.grid.card_table[grid[i]].set_orientation(
                    int(self.metadata['rotate' + str(i)]))
        self.win.mask(self._play_level)

    def write_file(self, file_path):
        """ Write the grid status to the Journal """
        self.metadata['play_mode'] = self._play_mode
        self.metadata['play_level'] = self._play_level
        for i in range(24):
            self.metadata['card' + str(i)] = str(self.win.grid.grid[i])
            self.metadata['rotate' + str(i)] = str(
                self.win.grid.card_table[self.win.grid.grid[i]].orientation)

    def _setup_toolbars(self, have_toolbox):
        """ Setup the toolbars.. """

        if have_toolbox:
            toolbox = ToolbarBox()

            # Activity toolbar
            activity_button = ActivityToolbarButton(self)

            toolbox.toolbar.insert(activity_button, 0)
            activity_button.show()

            self.set_toolbar_box(toolbox)
            toolbox.show()
            toolbar = toolbox.toolbar

        else:
            # Use pre-0.86 toolbar design
            games_toolbar = Gtk.Toolbar()
            toolbox = activity.ActivityToolbox(self)
            self.set_toolbox(toolbox)
            toolbox.add_toolbar(_('Game'), games_toolbar)
            toolbox.show()
            toolbox.set_current_toolbar(1)
            toolbar = games_toolbar

        # Add the buttons and labels to the toolbars
        self.level_button = button_factory(
            LEVEL_ICONS[self._play_level], toolbar, self.change_play_level_cb,
            tooltip=_('Set difficulty level.'))
        mode = self._play_mode
        mode += 1
        if mode == len(GAME_ICONS):
            mode = 0
        self.game_buttons = []
        for i in range(len(GAME_ICONS)):
            if i==0:
                self.game_buttons.append(radio_factory(
                        GAME_ICONS[0], toolbar, self.change_play_mode_cb,
                        cb_arg=0, tooltip=_('Select game.'), group=None))
            else:
                self.game_buttons.append(radio_factory(
                        GAME_ICONS[i], toolbar, self.change_play_mode_cb,
                        cb_arg=i, tooltip=_('Select game.'),
                        group=self.game_buttons[0]))
        self.game_buttons[mode].set_active(True)
        separator_factory(toolbar, False, True)
        self.status_label = label_factory(toolbar, _("drag to swap"), width=85)

        if _have_toolbox:
            separator_factory(toolbox.toolbar, True, False)

            stop_button = StopButton(self)
            stop_button.props.accelerator = '<Ctrl>q'
            toolbox.toolbar.insert(stop_button, -1)
            stop_button.show()

    def change_play_level_cb(self, button=None, play_level=None):
        """ Cycle between levels """
        if self._play_mode > 0:
            return
        if play_level is None:
            self._play_level += 1
            if self._play_level == len(LEVEL_ICONS):
                self._play_level = 0
        else:
            self._play_level = play_level
        self.level_button.set_icon_name(LEVEL_ICONS[self._play_level])
        self.win.grid.reset(GAME_ICONS[self._play_mode])
        self.win.mask(self._play_level)

    def change_play_mode_cb(self, button=None, play_mode=None):
        """ Cycle between game modes """
        if play_mode is None:
            self._play_mode += 1
            if self._play_mode == len(GAME_ICONS):
                self._play_mode = 0
        else:
            self._play_mode = play_mode
        mode = self._play_mode
        mode += 1
        if mode == len(GAME_ICONS):
            mode = 0
        if hasattr(self, 'win'):
            self.win.mode = GAME_ICONS[self._play_mode]
            self.win.grid.initialize_cards(self.win.sprites, self.win.path,
                                          self.win.card_dim, self.win.scale,
                                          GAME_ICONS[self._play_mode])
            if self._play_mode > 0:
                self._play_level = len(LEVEL_ICONS) - 1
                self.level_button.set_icon_name(LEVEL_ICONS[self._play_level])
                self.win.mask(self._play_level)
            self.win.grid.reset(GAME_ICONS[self._play_mode])
