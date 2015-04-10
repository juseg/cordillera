#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm
from paperglobals import *

# simulations used
res = '5km'
records = records[0:3:2]
offsets = offsets[0:3:2]
cislevs = [29.0, 29.0]

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

    # load extra output
    nc = open_extra_file(res, rec, offsets[i])
    x = nc.variables['x']
    y = nc.variables['y']
    thk = nc.variables['thk']
    icecover = (thk[:] >= thkth).sum(axis=0).T
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
    cs.clabel(fontsize=6, fmt='%i ka', manual=[(-1825e3, 1000e3)])
    ax.contour(x[:], y[:], icecover, [levs[0]], colors='k', linewidths=0.5)

    # close extra file
    nc.close()
    add_corner_tag(ax, rec.upper())

# locate major mountain ranges
txtkwa = dict(ha='center', va='center',
              bbox=dict(ec='k', fc='w', alpha=1.0),
              arrowprops=dict(arrowstyle="->"))
ax.annotate('AR', xy=(-2300e3, 2600e3), xytext=(-2000e3, 2600e3), **txtkwa)
ax.annotate('SM', xy=(-2000e3, 1450e3), xytext=(-2350e3, 1450e3), **txtkwa)
ax.annotate('CM', xy=(-1950e3,  700e3), xytext=(-2350e3,  700e3), **txtkwa)
ax.annotate('NC', xy=(-1900e3, 250e3), xytext=(-2350e3, 250e3), **txtkwa)
ax.annotate('WSEM', xy=(-2200e3, 2150e3), xytext=(-1200e3, 2150e3), **txtkwa)
ax.annotate('SMKM', xy=(-1550e3, 1900e3), xytext=(-1200e3, 1900e3), **txtkwa)
ax.annotate('NRM', xy=(-1600e3, 1450e3), xytext=(-1200e3, 1450e3), **txtkwa)
ax.annotate('CRM', xy=(-1550e3,  650e3), xytext=(-1200e3,  650e3), **txtkwa)

# add colorbar and save
cb = fig.colorbar(cf, ax.cax)
cb.set_label('Duration of ice cover (kyr)')
fig.savefig('duration')
