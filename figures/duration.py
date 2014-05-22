#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from iceplot import plot as iplt
from paperglobals import *

# simulations used
res = '10km'
records = ['grip', 'epica']
offsets = [5.8, 5.6]

# initialize figure
fig = iplt.gridfigure((47.5, 95.0), (1, len(records)), axes_pad=2.5*in2mm,
                      cbar_mode='single', cbar_pad=2.5*in2mm, cbar_size=5*in2mm)

# draw topo and coastline
draw_boot_topo(fig.grid, res)

# loop on records[i]
for i, rec in enumerate(records):
    print 'reading %s extra output...' % rec
    ax = fig.grid[i]
    this_run_path = run_path % (res, rec, offsets[i]*100)

    # load extra output
    nc = Dataset(this_run_path + '-extra.nc')
    mask = nc.variables['mask']
    x = nc.variables['x']
    y = nc.variables['y']
    icecover = (mask[:] == 2).sum(axis=0).T
    icecover *= 120.0/len(nc.variables['time'])

    # plot
    levs = range(0,121,20)
    levs[0] = 1e-6
    cf = ax.contourf(x, y, icecover, levels=levs, cmap='Greens', alpha=0.75)
    ax.contour(x, y, icecover, [levs[0]], colors='k')

    # close extra file
    annotate(ax, rec.upper())
    nc.close()

# add colorbar and save
cb = fig.colorbar(cf, ax.cax)
cb.set_label('Duration of ice cover (kyr)')
fig.savefig('duration.png')
