#!/usr/bin/env python

#Copyright (c) 2009,10 Walter Bender

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public
# License along with this library; if not, write to the
# Free Software Foundation, 51 Franklin Street, Suite 500 Boston, MA
# 02110-1335 USA

import os
from constants import C, H, RT

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
    j = '  <g transform="translate(0,-852.4)">\n'
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
    b = '         d="m 342.9,826.6 a 97.1,88.6 0 1 1 -194.3,0 97.1,88.6 0 1 1 194.3,0 z"\n'
    c = '         transform="matrix(0.76,0,0,0.84,' + x + ',' + y +')"\n'
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

def _svg_hex(top, left, right, rotate=0):
    """ draw a hexagon """
    a = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
    b = '<!-- Created with Python in Emacs -->\n'
    c = '<svg\n'
    d = '   xmlns:svg="http://www.w3.org/2000/svg"\n'
    e = '   xmlns="http://www.w3.org/2000/svg"\n'
    f = '   version="1.1"\n'
    g = '   width="202."\n'
    h = '   height="231.9"\n'
    i = '   id="hexagon">\n'
    if rotate == 120:
        j = '  <g transform="matrix(-0.5,-0.87,0.87,-0.5,-129.5,678.7)">\n'
    elif rotate == 240:
        j = '  <g transform="matrix(-0.5,0.87,-0.87,-0.5,703.5,34.5)">\n'
    else:
        j = '  <g transform="translate(-270.9,-365.2)">\n'
    k = '    <path\n'
    l = '       d="m 272.0,423.2 100.6,-57.5 99.4,57.5 -100.6,57.5 -99.4,-57.5 z"\n'
    m = '       style="fill:' + top + ';fill-opacity:1;stroke:#000000;stroke-width:4;stroke-linecap:butt;stroke-linejoin:round;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />\n'
    n = '    <path\n'
    o = '       d="m 371.5,596.6 -100.1,-58.3 0.1,-114.9 100.1,58.3 -0.1,114.9 z"\n'
    p = '       style="fill:' + left + '#0000ff;fill-opacity:1;stroke:#000000;stroke-width:4;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />\n'
    q = '    <path\n'
    r = '       d="m 372.6,596.3 100.1,-58.3 -0.1,-114.9 -100.1,58.3 0.1,114.9 z"\n'
    s = '       style="fill:' + right + ';fill-opacity:1;stroke:#000000;stroke-width:4;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />\n'
    t = '  </g>\n'
    u = '</svg>\n'
    return a + b + c + d + e + f + g + h + i + j + k + l + m + n + o + p + q +\
        r + s + t + u

def _svg_triangle(top, bottom, left, rotate=None):
    a = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
    b = '<!-- Created with Python in Emacs -->\n'
    c = '<svg\n'
    d = '   xmlns:svg="http://www.w3.org/2000/svg"\n'
    e = '   xmlns="http://www.w3.org/2000/svg"\n'
    f = '   version="1.1"\n'
    g = '   width="103.6" height="117.8">\n'
    if rotate == 60:
        rr1 = '<g\n     transform="matrix(0.5,0.87,-0.87,0.5,101.3,-2.4)">\n'
        rr2 = '</g>'
    elif rotate == 120:
        rr1 = '<g\n     transform="matrix(-0.5,0.87,-0.87,-0.5,105.1,58.0)">\n'
        rr2 = '</g>'
    elif rotate == 240:
        rr1 = '<g\n     transform="matrix(-0.5,-0.87,0.87,-0.5,1.7,118.7)">\n'
        rr2 = '</g>'
    elif rotate == 300:
        rr1 = '<g\n     transform="matrix(0.5,-0.87,0.87,0.5,-1.0,59.6)">\n'
        rr2 = '</g>'
    else:
        rr1 = ''
        rr2 = ''
    if rotate == 180:
        h = '  <g     transform="matrix(-1,0,0,-1,838.7,574.0)">\n'
    else:
        h = '  <g     transform="translate(-735.1,-456.2)">\n'
    i = '    <g      transform="translate(129.8,111.4)">\n'
    j = '      <path\n'
    k = '         d="m 607.8,460.4 98.2,-55.0 -65.6,-0.9 -32.7,55.9 z"\n'
    l = '         style="fill:' + bottom + ';fill-opacity:1;stroke:#000000;stroke-width:4;stroke-linecap:butt;stroke-linejoin:round;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />\n'
    m = '      <path\n'
    n = '         d="m 607.3,460.6 0,-113.5 33.3,56.7 -33.3,56.8 z"\n'
    o = '         style="fill:' + left + ';fill-opacity:1;stroke:#000000;stroke-width:4;stroke-linecap:butt;stroke-linejoin:round;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />\n'
    p = '      <path\n'
    q = '         d="m 706.9,405.2 -98.7,-58.4 32.3,57.2 66.4,1.2 z"\n'
    r = '         style="fill:' + top + ';fill-opacity:1;stroke:#000000;stroke-width:4;stroke-linecap:butt;stroke-linejoin:round;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />\n'
    s = '    </g>\n'
    t = '</g>\n'
    u = '</svg>\n'
    return a + b + c + d + e + f + g + rr1 + h + i + j + k + l + m + n + o + \
        p + q + r + s + t + rr2 + u

def open_file(datapath, filename):
    """ Create a file for writing """
    return file(os.path.join(datapath, filename), "w")


def generator(datapath):
    """ Make the cards: squares with circles, hexagons, and triangles """
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
        f = open_file(datapath, "hexagon-r0-%d.svg" % (i))
        f.write(_svg_hex(c[0], c[1], c[2]))
        f.close()
        f = open_file(datapath, "hexagon-r120-%d.svg" % (i))
        f.write(_svg_hex(c[0], c[1], c[2], 120))
        f.close()
        f = open_file(datapath, "hexagon-r240-%d.svg" % (i))
        f.write(_svg_hex(c[0], c[1], c[2], 240))
        f.close()

    for i, c in enumerate(RT):
        f = open_file(datapath, "triangle-r0-%d.svg" % (i))
        f.write(_svg_triangle(c[0], c[1], c[2]))
        f.close()
        f = open_file(datapath, "triangle-r60-%d.svg" % (i))
        f.write(_svg_triangle(c[0], c[1], c[2], rotate=60))
        f.close()
        f = open_file(datapath, "triangle-r120-%d.svg" % (i))
        f.write(_svg_triangle(c[0], c[1], c[2], rotate=120))
        f.close()
        f = open_file(datapath, "triangle-r180-%d.svg" % (i))
        f.write(_svg_triangle(c[0], c[1], c[2], rotate=180))
        f.close()
        f = open_file(datapath, "triangle-r240-%d.svg" % (i))
        f.write(_svg_triangle(c[0], c[1], c[2], rotate=240))
        f.close()
        f = open_file(datapath, "triangle-r300-%d.svg" % (i))
        f.write(_svg_triangle(c[0], c[1], c[2], rotate=300))
        f.close()

def main():
    """ Command line version for testing """
    return 0

if __name__ == "__main__":
    if not os.path.exists(os.path.join(os.path.abspath('.'), 'images')):
        os.mkdir(os.path.join(os.path.abspath('.'), 'images'))
    generator(os.path.join(os.path.abspath('.'), 'images'))
    main()
