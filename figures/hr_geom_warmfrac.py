#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt

# simulations used
res = '5km'
records = ut.records[ut.hrs]
offsets = ut.offsets[ut.hrs]

# initialize figure
figw, figh = 120.0, 100.0
fig, grid = iplt.subplots_mm(nrows=1, ncols=2, sharex=True, sharey=True,
                             figsize=(figw, figh),
                             left=2.5, right=20.0, bottom=2.5, top=2.5,
                             wspace=2.5, hspace=2.5)
cax = fig.add_axes([1-17.5/figw, 2.5/figh, 5.0/figw, 1-5.0/figh])

# draw topo and coastline
ut.pl.draw_boot_topo(grid, res)

# loop on records[i]
for i, rec in enumerate(records):
    print 'reading %s extra output...' % rec
    ax = grid[i]
    ax.set_rasterization_zorder(2.5)

    # read extra output
    nc = ut.io.open_extra_file(res, rec, offsets[i])
    x = nc.variables['x']
    y = nc.variables['y']
    w = (3*x[0]-x[1])/2
    e = (3*x[-1]-x[-2])/2 - (x[-1]-x[-2])/2  # weird but works
    n = (3*y[0]-y[1])/2
    s = (3*y[-1]-y[-2])/2 - (y[-1]-y[-2])/2  # weird but works
    thk = nc.variables['thk']
    temp = nc.variables['temppabase']

    # compute duration of warm-based coved
    warm = np.ma.array((temp[:] > -1e-9), mask=(thk[:] < ut.thkth))
    warm = warm.mean(axis=0).T

    # set levels, colors and hatches
    levs = [-1, 0.0, 0.5, 0.9, 0.99, 1.0]
    cmap = iplt.get_cmap('Reds')
    colors = cmap(np.linspace(0.0, 1.0, len(levs)-1))
    hatches = ['//'] + ['']*(len(levs)-2)

    # draw contours
    cs = ax.contourf(x[:], y[:], warm, levels=levs, alpha=0.75,
                            colors=colors, hatches=hatches)
    ax.contour(x[:], y[:], warm, [0.0],
                      colors='k', linewidths=0.25)
    ax.contour(x[:], y[:], warm.mask, [0.5],
                      colors='k', linewidths=0.5)

    # close extra file
    ut.pl.add_corner_tag(ax, rec.upper())
    nc.close()

# locate Skeena Mountains
ut.pl.add_pointer_tag(ax, 'SM', xy=(-2000e3, 1450e3), xytext=(-2350e3, 1450e3))
ut.pl.add_pointer_tag(ax, 'MKM', xy=(-1550e3, 2000e3), xytext=(-1200e3, 2000e3))

# add colorbar and save
cb = fig.colorbar(cs, cax, ticks=levs[1:])
cb.set_label('Fraction of warm-based ice cover')
fig.savefig('hr_geom_warmfrac')
