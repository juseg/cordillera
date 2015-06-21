#!/usr/bin/env python2
# coding: utf-8

import os
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation as mani
from matplotlib.colors import LogNorm
from paperglobals import *

# parameters
res = '5km'
records = records[0:3:2]
offsets = offsets[0:3:2]

# drawing function for animations
def draw(ax, idx):
    t = nc.variables['time'][idx]*s2ka
    print 'plotting %s at %s ka...' % (rec, t)
    ax.cla()

    # plot
    iplt.imshow(nc, 'topg', idx, ax, thkth=thkth,
                cmap=topo_cmap, norm=topo_norm)
    iplt.icemargin(nc, idx, ax, thkth=thkth,
                   linewidths=0.5)
    iplt.contour(nc, 'usurf', idx, ax, thkth=thkth,
                 levels=range(200, 5000, 200),
                 cmap=None, colors='k', linewidths=0.1)
    iplt.contour(nc, 'usurf', idx, ax, thkth=thkth,
                 levels=range(1000, 5000, 1000),
                 cmap=None, colors='k', linewidths=0.25)
    im = iplt.imshow(nc, 'velsurf_mag', idx, ax, thkth=thkth,
                     cmap=vel_cmap, norm=vel_norm, alpha=0.75)
    add_corner_tag(ax, '%s, %s ka' % (rec.upper(), -t))
    
    # return mappable for colorbar
    return im

# loop on records
for i, rec in enumerate(records):

    # load data
    nc = open_extra_file(res, rec, offsets[i])

    # initialize figure
    fig = iplt.simplefigure((47.51, 95.01), axes_pad=2.5*in2mm,
                          cbar_mode='single', cbar_pad=2.5*in2mm, cbar_size=5*in2mm)
    ax = plt.axes(fig.grid[0])

    # draw first frame and colorbar
    im = draw(ax, 0)
    cb = fig.colorbar(im, ax.cax, extend='both', format='%i',
                     ticks=np.logspace(1, 3.5, 6))
    cb.set_label(r'surface velocity ($m\,yr^{-1}$)', labelpad=-2.0)

    # save individual frames
    for idx in range(1200):
        draw(ax, idx)
        fig.savefig('frames/%s-%04i.png' % (rec, idx))

    # close nc file
    nc.close()