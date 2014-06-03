#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm
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
    u = nc.variables['uvelbase']
    v = nc.variables['uvelbase']
    c = (u[:]**2 + v[:]**2)**0.5
    dist = c.sum(axis=0).T*100.0

    # plot
    levs = np.logspace(4, 9, 6)
    cmap = plt.get_cmap('CMRmap')
    colors=cmap(np.linspace(0, 1, len(levs)-1))
    cf = ax.contourf(x[:], y[:], dist, levels=levs, alpha=0.75,  # extend='both',
                     cmap='Reds', norm=BoundaryNorm(levs, 256))
    ax.contour(x[:], y[:], dist.mask, [0.5], colors='k')

    # close extra file
    annotate(ax, rec.upper())
    nc.close()

# add colorbar and save
cb = fig.colorbar(cf, ax.cax, format='%.0e')
cb.set_label('Cumulative basal displacement (m)')
fig.savefig('erosion.png')
