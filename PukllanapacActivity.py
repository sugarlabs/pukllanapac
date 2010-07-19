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

import sugar
from sugar.activity import activity
try: # 0.86+ toolbar widgets
    from sugar.bundle.activitybundle import ActivityBundle
    from sugar.activity.widgets import ActivityToolbarButton
    from sugar.activity.widgets import StopButton
    from sugar.graphics.toolbarbox import ToolbarBox
    from sugar.graphics.toolbarbox import ToolbarButton
    _new_sugar_system = True
except ImportError:
    _new_sugar_system = False
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.menuitem import MenuItem
from sugar.graphics.icon import Icon
from sugar.datastore import datastore

from gettext import gettext as _
import locale
import os.path

from sprites import *
from window import Game

SERVICE = 'org.sugarlabs.PukllanapacActivity'
IFACE = SERVICE
PATH = '/org/augarlabs/PukllanapacActivity'
LEVEL_ICONS = ['level1', 'level2', 'level3']


def _button_factory(icon_name, tooltip, callback, toolbar, cb_arg=None,
                    accelerator=None):
    """Factory for making toolbar buttons"""
    my_button = ToolButton(icon_name)
    my_button.set_tooltip(tooltip)
    my_button.props.sensitive = True
    if accelerator is not None:
        my_button.props.accelerator = accelerator
    if cb_arg is not None:
        my_button.connect('clicked', callback, cb_arg)
    else:
        my_button.connect('clicked', callback)
    if hasattr(toolbar, 'insert'):  # the main toolbar
        toolbar.insert(my_button, -1)
    else:  # or a secondary toolbar
        toolbar.props.page.insert(my_button, -1)
    my_button.show()
    return my_button


def _label_factory(label, toolbar):
    """ Factory for adding a label to a toolbar """
    my_label = gtk.Label(label)
    my_label.set_line_wrap(True)
    my_label.show()
    _toolitem = gtk.ToolItem()
    _toolitem.add(my_label)
    toolbar.insert(_toolitem, -1)
    _toolitem.show()
    return my_label


def _separator_factory(toolbar, visible=True, expand=False):
    """ Factory for adding a separator to a toolbar """
    _separator = gtk.SeparatorToolItem()
    _separator.props.draw = visible
    _separator.set_expand(expand)
    toolbar.insert(_separator, -1)
    _separator.show()


class PukllanapacActivity(activity.Activity):
    """ Sliding puzzle game """

    def __init__(self, handle):
        """ Initialize the toolbars and the game board """
        super(PukllanapacActivity,self).__init__(handle)

        self._play_level = 0
        self._setup_toolbars(_new_sugar_system)

        # Create a canvas
        canvas = gtk.DrawingArea()
        canvas.set_size_request(gtk.gdk.screen_width(), \
                                gtk.gdk.screen_height())
        self.set_canvas(canvas)
        canvas.show()
        self.show_all()

        # Initialize the canvas
        self.tw = Game(canvas, os.path.join(activity.get_bundle_path(),
                                            'images'), self)

        # Restore game state from Journal or start new game
        try:  # Try reading restored settings from the Journal.
            self._play_level = int(self.metadata['play_level'])
            grid = []
            for i in range(24):
                grid.append(int(self.metadata['card'+str(i)]))
            self._play_level = int(self.metadata['play_level'])
            # print "restoring: " + str(grid)
            self.tw.grid.set_grid(grid)
        except KeyError:
            pass
        print "restoring play level %d " % (self._play_level)
        self.tw.mask(self._play_level)

    def write_file(self, file_path):
        """ Write the grid status to the Journal """
        self.metadata['play_level'] = self._play_level
        # print "saving " + str(self.tw.grid.grid)
        for i in range(24):
            self.metadata['card'+str(i)] = str(self.tw.grid.grid[i])

    def _setup_toolbars(self, new_sugar_system):
        """ Setup the toolbars.. """

        if new_sugar_system:
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
            games_toolbar = gtk.Toolbar()
            toolbox = activity.ActivityToolbox(self)
            self.set_toolbox(toolbox)
            toolbox.add_toolbar(_('Game'), games_toolbar)
            toolbox.show()
            toolbox.set_current_toolbar(1)
            toolbar = games_toolbar

        # Add the buttons and labels to the toolbars
        self.level_button = _button_factory(LEVEL_ICONS[self._play_level],
                                            _('Set difficulty level.'),
                                            self.level_cb, toolbar)
        _separator_factory(toolbar, True, False)
        self.status_label = _label_factory(_("drag to swap"), toolbar)

        if _new_sugar_system:
            _separator_factory(toolbox.toolbar, False, True)

            stop_button = StopButton(self)
            stop_button.props.accelerator = '<Ctrl>q'
            toolbox.toolbar.insert(stop_button, -1)
            stop_button.show()

    def level_cb(self, button):
        """ Cycle between levels """
        self._play_level += 1
        if self._play_level == len(LEVEL_ICONS):
            self._play_level = 0
        self.level_button.set_icon(LEVEL_ICONS[self._play_level])
        self.tw.grid.reset()
        self.tw.mask(self._play_level)
