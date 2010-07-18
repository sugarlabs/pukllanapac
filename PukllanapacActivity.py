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
except ImportError:
    pass
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


class PukllanapacActivity(activity.Activity):
    """ Sliding puzzle game """

    def __init__(self, handle):
        """ Initialize the toolbars and the game board """
        super(PukllanapacActivity,self).__init__(handle)

        try:
            # Use 0.86 toolbar design
            toolbar_box = ToolbarBox()

            # Buttons added to the Activity toolbar
            activity_button = ActivityToolbarButton(self)
            toolbar_box.toolbar.insert(activity_button, 0)
            activity_button.show()

            # Label for showing status
            self.results_label = gtk.Label(_("drag to swap"))
            self.results_label.show()
            results_toolitem = gtk.ToolItem()
            results_toolitem.add(self.results_label)
            toolbar_box.toolbar.insert(results_toolitem,-1)

            separator = gtk.SeparatorToolItem()
            separator.props.draw = False
            separator.set_expand(True)
            separator.show()
            toolbar_box.toolbar.insert(separator, -1)

            # The ever-present Stop Button
            stop_button = StopButton(self)
            stop_button.props.accelerator = '<Ctrl>Q'
            toolbar_box.toolbar.insert(stop_button, -1)
            stop_button.show()

            self.set_toolbar_box(toolbar_box)
            toolbar_box.show()

        except NameError:
            # Use pre-0.86 toolbar design
            self.toolbox = activity.ActivityToolbox(self)
            self.set_toolbox(self.toolbox)

            self.projectToolbar = ProjectToolbar(self)
            self.toolbox.add_toolbar( _('Project'), self.projectToolbar )

            self.toolbox.show()

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
            print "restoring: " + str(grid)
            self.tw.grid.set_grid(grid)
        except KeyError:
            pass
        self.tw.grid.show_all()

    def write_file(self, file_path):
        """ Write the grid status to the Journal """
        self.metadata['play_level'] = '2'
        print "saving " + str(self.tw.grid.grid)
        for i in range(24):
            self.metadata['card'+str(i)] = str(self.tw.grid.grid[i])


class ProjectToolbar(gtk.Toolbar):
    """ Project toolbar for pre-0.86 toolbars """

    def __init__(self, pc):
        """ Initialize a project toolbar """
        gtk.Toolbar.__init__(self)
        self.activity = pc

        # Label for showing status
        self.activity.results_label = gtk.Label(\
            _("drag to swap"))
        self.activity.results_label.show()
        self.activity.results_toolitem = gtk.ToolItem()
        self.activity.results_toolitem.add(self.activity.results_label)
        self.insert(self.activity.results_toolitem, -1)
        self.activity.results_toolitem.show()
