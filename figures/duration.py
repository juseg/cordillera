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
cislevs = [28.0, 29.0]

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

    # set contour levels, colors and hatches
    levs = range(0, 21, 5) + [cislevs[i]] + range(40,121,20)
    levs[0] = 1e-6
    cmap = plt.get_cmap('RdBu')
    colors = cmap(np.hstack((np.linspace(0.0, 0.5, (len(levs)-1)/2),
                             np.linspace(0.5, 1.0, (len(levs)-1)/2))))
    hatches = ['']*5 + ['//'] + ['']*4

    # plot
    cf = ax.contourf(x[:], y[:], icecover, levels=levs, alpha=0.75,
                     colors=colors, hatches=hatches)
    cs = ax.contour(x[:], y[:], icecover, [cislevs[i]], colors='k', linewidths=0.25)
    cs.clabel(fontsize=4, fmt='%i kyr', manual=[(-1825e3, 1000e3)])
    ax.contour(x[:], y[:], icecover, [levs[0]], colors='k', linewidths=0.5)

    # close extra file
    nc.close()
    annotate(ax, rec.upper())

# add colorbar and save
cb = fig.colorbar(cf, ax.cax)
cb.set_label('Duration of ice cover (kyr)')
fig.savefig('duration.png')
