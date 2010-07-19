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

import os

XCOR = ["-188.17646", "11.823541"]
YCOR = ["162.71119", "362.71119"]

R = "#ff0000"
Y = "#ffff00"
B = "#0000ff"

C = [[Y, B, Y, R], [R, Y, Y, R], [R, R, Y, R], [R, R, R, R], [B, B, B, Y], [Y, B, Y, Y],
     [R, B, R, R], [Y, Y, Y, Y], [Y, Y, R, B], [Y, Y, B, B], [Y, R, Y, Y], [R, R, Y, B],
     [B, B, B, B], [R, B, B, B], [B, R, B, R], [B, B, R, R], [R, R, B, Y], [B, Y, B, Y],
     [R, Y, Y, B], [R, B, B, Y], [Y, R, B, R], [R, Y, R, Y], [R, B, Y, B], [Y, B, B, R]]

def _svg_header():
    """ the common header every card shares """
    a = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
    b = '<!-- Created with Python in Emacs -->\n'
    c = '<svg\n'
    d = '   xmlns:svg="http://www.w3.org/2000/svg"\n'
    e = '   xmlns="http://www.w3.org/2000/svg"\n'
    f = '   version="1.1"\n'
    g = '   width="200"\n'
    h = '   height="200"\n'
    i = '   id="svg2">\n'
    j = '  <g transform="translate(0,-852.36218)">\n'
    k = '      <rect\n'
    l = '         width="200"\n'
    m = '         height="200"\n'
    n = '         x="0"\n'
    o = '         y="852.36218"\n'
    p = '         style="fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:#000000;stroke-opacity:1" />\n'
    return a + b + c + d + e + f + g + h + i + j + k + l + m + n + o + p


def _svg_circle(x, y):
    """ draw an arc at x, y """
    a = '      <path\n'
    b = '         d="m 342.85714,826.64789 a 97.14286,88.571426 0 1 1 -194.28572,0 97.14286,88.571426 0 1 1 194.28572,0 z"\n'
    c = '         transform="matrix(0.76176468,0,0,0.83548389,' + x + ',' + y +')"\n'
    return a + b + c


def _svg_upper_right(color):
    """ draw an arc in the upper right quadrant """
    a = _svg_circle(XCOR[0], YCOR[0])
    b = '         style="fill:' + color + ';fill-opacity:1;fill-rule:nonzero;stroke:none" />\n'
    return a + b


def _svg_lower_right(color):
    """ draw an arc in the upper right quadrant """
    a = _svg_circle(XCOR[0], YCOR[1])
    b = '         style="fill:' + color + ';fill-opacity:1;fill-rule:nonzero;stroke:none" />\n'
    return a + b


def _svg_upper_left(color):
    """ draw an arc in the upper right quadrant """
    a = _svg_circle(XCOR[1], YCOR[0])
    b = '         style="fill:' + color + ';fill-opacity:1;fill-rule:nonzero;stroke:none" />\n'
    return a + b


def _svg_lower_left(color):
    """ draw an arc in the upper right quadrant """
    a = _svg_circle(XCOR[1], YCOR[1])
    b = '         style="fill:' + color + ';fill-opacity:1;fill-rule:nonzero;stroke:none" />\n'
    return a + b


def _svg_footer():
    """ A common footer """
    a = '  </g>\n'
    b = '</svg>\n'
    return a + b


def open_file(datapath, filename):
    """ Create a file for writing """
    return file(os.path.join(datapath, filename), "w")


def generator(datapath):
    """ Make all of the cards """
    for i, c in enumerate(C):
        f = open_file(datapath, "card-%d.svg" % (i))
        svg = _svg_header()
        svg += _svg_upper_left(c[0])
        svg += _svg_lower_left(c[1])
        svg += _svg_lower_right(c[2])
        svg += _svg_upper_right(c[3])
        svg += _svg_footer()
        f.write(svg)
        f.close()


def main():
    """ Command line version for testing """
    return 0

if __name__ == "__main__":
    if not os.path.exists(os.path.join(os.path.abspath('.'), 'images')):
        os.mkdir(os.path.join(os.path.abspath('.'), 'images'))
    generator(os.path.join(os.path.abspath('.'), 'images'))
    main()
