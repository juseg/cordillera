#!/usr/bin/env python2
# coding: utf-8

"""Plotting tools."""

import util as ut

import os
import numpy as np
from iceplotlib import plot as iplt
from matplotlib.transforms import ScaledTranslation

# unit conversion
in2mm = 1/25.4
pt2mm = 72*in2mm

def add_corner_tag(ax, s, ha='right', va='top'):
    fig = ax.get_figure()
    x = (ha == 'right')  # 0 for left edge, 1 for right edge
    y = (va == 'top')  # 0 for bottom edge, 1 for top edge
    xoffset = (1 - 2*x)*2.5*in2mm
    yoffset = (1 - 2*y)*2.5*in2mm
    offset = ScaledTranslation(xoffset, yoffset, fig.dpi_scale_trans)
    return ax.text(x, y, s, ha=ha, va=va,
                   bbox=dict(ec='k', fc='w', pad=1.25*pt2mm),
                   transform=ax.transAxes + offset)


def add_pointer_tag(ax, s, xy, xytext):
    return ax.annotate(s, xy=xy, xytext=xytext, ha='center', va='center',
                       xycoords='data', textcoords='data',
                       bbox=dict(ec='k', fc='w', boxstyle='square'),
                       arrowprops=dict(arrowstyle="->"))


def draw_boot_topo(grid, res):
    nc = ut.io.open_boot_file(res)
    for ax in grid.flat:
        im = nc.imshow('topg', ax=ax, cmap=ut.topo_cmap, norm=ut.topo_norm)
    nc.close()
    return im


def draw_coastline(grid, res):
    nc = ut.io.open_boot_file(res)
    for ax in grid.flat:
        cs = nc.contour('topg', ax=ax, levels=[0.0],
                        cmap=None, colors='k', linewidths=0.5)
    nc.close()
    return cs
