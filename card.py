#Copyright (c) 2010, 2011 Walter Bender

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public
# License along with this library; if not, write to the
# Free Software Foundation, 51 Franklin Street, Suite 500 Boston, MA
# 02110-1335 USA

from gi.repository.GdkPixbuf import Pixbuf

from sprites import Sprite


def load_image(file, w, h):
    """ Convert from file to pixbuf at size w, h """
    return Pixbuf.new_from_file_at_size(file, int(w), int(h))


class Card:
    """ Class for defining individual cards """

    def __init__(self, sprites, path, card_dim, scale, c, x, y, shape='circle'):
        """ Load a card from a precomputed SVG. """
        self.images = []
        self.orientation = 0

        if shape == 'triangle':
            file = "%s/triangle-r0-%d.svg" % (path, c)
            self.increment = 60
        elif shape == 'hexagon':
            file = "%s/hexagon-r0-%d.svg" % (path, c)
            self.increment = 120
        else:
            file = "%s/card-%d.svg" % (path, c)
            self.increment = 90

        self.images.append(load_image(file, card_dim * scale,
                                      card_dim * scale))

        if shape == 'triangle':
            file = "%s/triangle-r60-%d.svg" % (path, c)
            self.images.append(load_image(file, card_dim * scale,
                                          card_dim * scale))
            file = "%s/triangle-r120-%d.svg" % (path, c)
            self.images.append(load_image(file, card_dim * scale,
                                          card_dim * scale))
            file = "%s/triangle-r180-%d.svg" % (path, c)
            self.images.append(load_image(file, card_dim * scale,
                                          card_dim * scale))
            file = "%s/triangle-r240-%d.svg" % (path, c)
            self.images.append(load_image(file, card_dim * scale,
                                          card_dim * scale))
            file = "%s/triangle-r300-%d.svg" % (path, c)
            self.images.append(load_image(file, card_dim * scale,
                                          card_dim * scale))
        elif shape == 'hexagon':
            file = "%s/hexagon-r120-%d.svg" % (path, c)
            self.images.append(load_image(file, card_dim * scale,
                                          card_dim * scale))
            file = "%s/hexagon-r240-%d.svg" % (path, c)
            self.images.append(load_image(file, card_dim * scale,
                                          card_dim * scale))
        else:
            for r in range(3):
                self.images.append(self.images[r].rotate_simple(90))

        # create sprite from svg file
        self.spr = Sprite(sprites, x, y, self.images[0])

    def reset_image(self, tw):
        """ Reset image to orientation 0. """
        while self.orientation != 0:
            self.rotate_ccw()

    def set_orientation(self, r):
        """ Set orientation to 0, 90, 180, or 270. """
        if r in [0, 60, 90, 120, 180, 240, 270, 300]:
            while r != self.orientation:
                self.rotate_ccw()

    def rotate_180(self):
        """ Rotate a tile 180 degrees """
        print "rotate 180"
        r = 0
        while r < 180:
            self.rotate_ccw()
            r += self.increment

    def rotate_ccw(self):
        """ Set the card image to correspond to rotation r. """
        self.orientation += self.increment
        if self.orientation == 360:
            self.orientation = 0
        self.spr.set_shape(self.images[int(self.orientation/self.increment)])
