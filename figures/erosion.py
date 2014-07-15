#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm, LogNorm
from paperglobals import *

# simulations used
res = '6km'
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
    w = (3*x[0]-x[1])/2
    e = (3*x[-1]-x[-2])/2 - (x[-1]-x[-2])/2  # weird but works
    n = (3*y[0]-y[1])/2
    s = (3*y[-1]-y[-2])/2 - (y[-1]-y[-2])/2  # weird but works
    c = nc.variables['velbase_mag']
    c = np.ma.array(c[:], mask=(mask[:] != 2))
    dist = c.sum(axis=0).T/10.0  # convert to km

    # set levels, colors and hatches
    levs = np.logspace(1.0, 4.5, 8)
    print levs
    cmap = plt.get_cmap('Reds')
    cols = cmap(np.linspace(0.0, 1.0, len(levs)+1))
    hatches = ['//'] + ['']*len(levs)

    # plot
    cf = ax.contourf(x[:], y[:], dist, levels=levs,
                     colors=cols, hatches=hatches,
                     extend='both', alpha=0.75)
    ax.contour(x[:], y[:], dist, levels=[levs[0]],
                     colors='k', linewidths=0.25)
    ax.contour(x[:], y[:], dist.mask, [0.5], colors='k', linewidths=0.5)

    # close extra file
    annotate(ax, rec.upper())
    nc.close()

# add colorbar and save
cb = fig.colorbar(cf, ax.cax, format='%i')
cb.set_label('Cumulative basal displacement (km)')
fig.savefig('erosion.png')
