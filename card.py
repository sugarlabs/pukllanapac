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

from sprites import Sprite


def load_image(file, w, h):
    """ convert from file to pixbuf at size w, h """
    return gtk.gdk.pixbuf_new_from_file_at_size(file, int(w), int(h))


class Card:
    """ class for defining individual cards """

    def __init__(self, tw, c, x, y):
        """ Load a card from a precomputed svg """
        self.images = []
        file = "%s/card-%d.svg" % (tw.path, c)
        self.images.append(load_image(file, tw.card_dim * tw.scale,
                                                 tw.card_dim * tw.scale))
        # create sprite from svg file
        self.spr = Sprite(tw.sprites, x, y, self.images[0])
        self.spr.draw()
