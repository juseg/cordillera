#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt

# simulations used
records = ut.hr.records
offsets = ut.hr.offsets

# initialize figure
fig, grid, cax = ut.pl.subplots_2_cax()

# draw topo and coastline
ut.pl.draw_boot_topo(grid)
ut.pl.draw_coastline(grid)

# loop on records[i]
for i, rec in enumerate(records):
    dt = offsets[i]
    ax = grid[i]
    ut.pl.draw_ne_vectors(ax)

    # load extra output
    nc = ut.io.load('output/0.7.2-craypetsc/cordillera-narr-5km/'
                    '%s3222cool%03d+ccyc4+till1545/y???????-extra.nc'
                     % (rec, round(100*dt)))
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
ut.pl.savefig(fig)
