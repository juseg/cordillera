#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm, LogNorm
from mpl_toolkits.axes_grid1.axes_grid import ImageGrid
from paperglobals import *

# parameters
res = '5km'
records = records[0:3:2]
offsets = offsets[0:3:2]

def icemaps(mis):
    # initialize figure
    fig = iplt.gridfigure((47.5, 95.0), (1, len(records)), axes_pad=2.5*in2mm,
                          cbar_mode='single', cbar_pad=2.5*in2mm, cbar_size=5*in2mm)

    # loop on records
    for i, rec in enumerate(records):
        ax = fig.grid[i]
        ax.set_rasterization_zorder(2.5)
        this_run_path = run_path % (res, rec, offsets[i]*100)

        # get ice volume maximum
        t = get_mis_times(this_run_path + '-ts.nc')[-1][1-mis]

        # load extra output
        nc = ncopen(this_run_path + '-extra.nc')
        time = nc.variables['time'][:]*s2ka

        # round maximum time to nearest slice
        idx = (np.abs(time[:]-t)).argmin()

        print 'plotting %s at %s ka...' % (rec, t)
        ax = fig.grid[i]
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
        annotate(ax, '%s, %s kyr' % (rec.upper(), t))

    # close extra file
    nc.close()

    # add colorbar and return figure
    cb = fig.colorbar(im, ax.cax, extend='both', format='%i',
                  ticks=np.logspace(1, 3.5, 6))
    cb.set_label(r'surface velocity ($m\,yr^{-1}$)', labelpad=-2.0)
    return fig
