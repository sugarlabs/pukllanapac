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
from constants import C, H, RT, LT

XCOR = ["-188.17646", "11.823541"]
YCOR = ["162.71119", "362.71119"]


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

def _svg_hex(top, left, right):
    """ draw a hexagon """
    a = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
    b = '<!-- Created with Python in Emacs -->\n'
    c = '<svg\n'
    d = '   xmlns:svg="http://www.w3.org/2000/svg"\n'
    e = '   xmlns="http://www.w3.org/2000/svg"\n'
    f = '   version="1.1"\n'
    g = '   width="202.28767"\n'
    h = '   height="231.94138"\n'
    i = '   id="hexagon">\n'
    j = '  <g transform="translate(-270.9034,-365.15558)">\n'
    k = '    <path\n'
    l = '       d="m 272.04724,423.15558 100.55096,-57.5 99.44904,57.5 -100.55096,57.5 -99.44904,-57.5 z"\n'
    m = '       style="fill:' + top + ';fill-opacity:1;stroke:#000000;stroke-width:4;stroke-linecap:butt;stroke-linejoin:round;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />\n'
    n = '    <path\n'
    o = '       d="m 371.47534,596.59696 -100.07194,-58.32969 0.0719,-114.87539 100.07194,58.32969 -0.0719,114.87539 z"\n'
    p = '       style="fill:' + left + '#0000ff;fill-opacity:1;stroke:#000000;stroke-width:4;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />\n'
    q = '    <path\n'
    r = '       d="m 372.61914,596.3201 100.07194,-58.32969 -0.0719,-114.87539 -100.07194,58.32969 0.0719,114.87539 z"\n'
    s = '       style="fill:' + right + ';fill-opacity:1;stroke:#000000;stroke-width:4;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />\n'
    t = '  </g>\n'
    u = '</svg>\n'
    return a + b + c + d + e + f + g + h + i + j + k + l + m + n + o + p + q +\
        r + s + t + u

def _svg_triangle(top, bottom, left, flip=False):
    a = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
    b = '<!-- Created with Python in Emacs -->\n'
    c = '<svg\n'
    d = '   xmlns:svg="http://www.w3.org/2000/svg"\n'
    e = '   xmlns="http://www.w3.org/2000/svg"\n'
    f = '   version="1.1"\n'
    g = '   id="triange">\n'
    if flip:
        h = '  <g     transform="matrix(-1,0,0,1,838.68554,-456.19895)">\n'
    else:
        h = '  <g     transform="translate(-735.12125,-456.19895)">\n'
    i = '    <g      transform="translate(129.81785,111.40982)">\n'
    j = '      <path\n'
    k = '         d="m 607.82135,460.38159 98.22306,-54.95995 -65.57024,-0.92468 -32.65282,55.88463 z"\n'
    l = '         style="fill:' + bottom + ';fill-opacity:1;stroke:#000000;stroke-width:4;stroke-linecap:butt;stroke-linejoin:round;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />\n'
    m = '      <path\n'
    n = '         d="m 607.3034,460.58514 0,-113.47935 33.29261,56.63592 -33.29261,56.84343 z"\n'
    o = '         style="fill:' + left + ';fill-opacity:1;stroke:#000000;stroke-width:4;stroke-linecap:butt;stroke-linejoin:round;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />'
    p = '      <path\n'
    q = '         d="m 706.86769,405.18383 -98.70613,-58.3947 32.3358,57.2359 66.37033,1.1588 z"\n'
    r = '         style="fill:' + top + ';fill-opacity:1;stroke:#000000;stroke-width:4;stroke-linecap:butt;stroke-linejoin:round;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />\n'
    s = '    </g>\n'
    t = '</g>\n'
    u = '</svg>\n'
    return a + b + c + d + e + f + g + h + i + j + k + l + m + n + o + p + q +\
        r + s + t + u

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

    for i, c in enumerate(H):
        f = open_file(datapath, "hex-%d.svg" % (i))
        f.write(_svg_hex(c[0], c[1], c[2]))
        f.close()

    for i, c in enumerate(RT):
        f = open_file(datapath, "triangle-r-%d.svg" % (i))
        f.write(_svg_triangle(c[0], c[1], c[2]))
        f.close()

    for i, c in enumerate(LT):
        f = open_file(datapath, "triangle-l-%d.svg" % (i))
        f.write(_svg_triangle(c[0], c[1], c[2], flip=True))
        f.close()

def main():
    """ Command line version for testing """
    return 0

if __name__ == "__main__":
    if not os.path.exists(os.path.join(os.path.abspath('.'), 'images')):
        os.mkdir(os.path.join(os.path.abspath('.'), 'images'))
    generator(os.path.join(os.path.abspath('.'), 'images'))
    main()
