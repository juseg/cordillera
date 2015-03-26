#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm, LogNorm
from paperglobals import *

# simulations used
res = '5km'
records = records[0:3:2]
offsets = offsets[0:3:2]

# initialize figure
fig = iplt.gridfigure((47.5, 95.0), (1, len(records)), axes_pad=2.5*in2mm,
                      cbar_mode='single', cbar_pad=2.5*in2mm, cbar_size=5*in2mm)

# draw topo and coastline
draw_boot_topo(fig.grid, res)

# loop on records[i]
for i, rec in enumerate(records):
    print 'reading %s extra output...' % rec
    ax = fig.grid[i]
    ax.set_rasterization_zorder(2.5)
    this_run_path = run_path % (res, rec, offsets[i]*100)

    # read extra output
    nc = ncopen(this_run_path + '-extra.nc')
    x = nc.variables['x']
    y = nc.variables['y']
    w = (3*x[0]-x[1])/2
    e = (3*x[-1]-x[-2])/2 - (x[-1]-x[-2])/2  # weird but works
    n = (3*y[0]-y[1])/2
    s = (3*y[-1]-y[-2])/2 - (y[-1]-y[-2])/2  # weird but works
    thk = nc.variables['thk']
    temp = nc.variables['temppabase']

    # compute duration of warm-based coved
    warm = np.ma.array((temp[:] > -1e-9), mask=(thk[:] < thkth))
    warm = warm.mean(axis=0).T

    # set levels, colors and hatches
    levs = [-1, 0.0, 0.5, 0.9, 0.99, 1.0]
    cmap = plt.get_cmap('Reds')
    colors = cmap(np.linspace(0.0, 1.0, len(levs)-1))
    hatches = ['//'] + ['']*(len(levs)-2)

    # draw contours
    cs = ax.contourf(x[:], y[:], warm, levels=levs, alpha=0.75,
                     colors=colors, hatches=hatches)
    ax.contour(x[:], y[:], warm, [0.0], colors='k', linewidths=0.25)
    ax.contour(x[:], y[:], warm.mask, [0.5], colors='k', linewidths=0.5)

    # close extra file
    annotate(ax, rec.upper())
    nc.close()

# locate Skeena Mountains
txtkwa = dict(ha='center', va='center',
              bbox=dict(ec='k', fc='w', alpha=1.0),
              arrowprops=dict(arrowstyle="->"))
ax.annotate('SM', xy=(-2000e3, 1450e3), xytext=(-2350e3, 1450e3), **txtkwa)
ax.annotate('MKM', xy=(-1550e3, 2000e3), xytext=(-1200e3, 2000e3), **txtkwa)

# add colorbar and save
cb = fig.colorbar(cs, ax.cax, ticks=levs[1:])
cb.set_label('Fraction of warm-based ice cover')
fig.savefig('warmfrac')
