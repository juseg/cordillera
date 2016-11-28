#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt

# simulations used
res = '5km'
records = ut.hr.records
offsets = ut.hr.offsets

# initialize figure
figw, figh = 85.0, 95.0
fig, grid = iplt.subplots_mm(nrows=1, ncols=2, sharex=True, sharey=True,
                             figsize=(figw, figh), projection=ut.pl.proj,
                             left=2.5, right=2.5, bottom=15.0, top=2.5,
                             wspace=2.5, hspace=2.5)
cax = fig.add_axes([2.5/figw, 7.5/figh, 1-5.0/figw, 5.0/figh])

# draw topo and coastline
ut.pl.draw_boot_topo(grid, res)
ut.pl.draw_coastline(grid, res)

# loop on records[i]
for i, rec in enumerate(records):
    print 'reading %s extra output...' % rec
    ax = grid[i]
    ax.set_rasterization_zorder(2.5)
    ut.pl.draw_ne_vectors(ax)

    # load extra output
    nc = ut.io.open_extra_file(res, rec, offsets[i])
    thk = nc.variables['thk']
    x = nc.variables['x']
    y = nc.variables['y']
    w = (3*x[0]-x[1])/2
    e = (3*x[-1]-x[-2])/2 - (x[-1]-x[-2])/2  # weird but works
    n = (3*y[0]-y[1])/2
    s = (3*y[-1]-y[-2])/2 - (y[-1]-y[-2])/2  # weird but works
    c = nc.variables['velbase_mag']
    c = np.ma.array(c[:], mask=(thk[:] < ut.thkth))
    dist = c.sum(axis=0).T/10.0  # convert to km

    # set levels, colors and hatches
    levs = np.logspace(1.0, 4.5, 8)
    cmap = iplt.get_cmap('Reds')
    cols = cmap(np.linspace(0.0, 1.0, len(levs)+1))
    hatches = ['//'] + ['']*len(levs)

    # plot
    cf = ax.contourf(x[:], y[:], dist, levels=levs,
                            colors=cols, hatches=hatches,
                            extend='both', alpha=0.75)
    ax.contour(x[:], y[:], dist, levels=[levs[0]],
                      colors='k', linewidths=0.25)
    ax.contour(x[:], y[:], dist.mask, [0.5],
                      colors='k', linewidths=0.5)

    # close extra file
    ut.pl.add_corner_tag(ax, rec.upper())
    nc.close()

# add colorbar and save
cb = fig.colorbar(cf, cax, orientation='horizontal', format='%i')
cb.set_label('cumulative basal displacement (km)')
fig.savefig('hr_geom_basedispl')