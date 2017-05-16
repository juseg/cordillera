#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt

# initialize figure
fig, grid, cax = ut.pl.subplots_2_cax()

# loop on records
for i, rec in enumerate(ut.ciscyc_hr_records):
    dt = ut.ciscyc_hr_offsets[i]
    ax = grid[i]

    # read extra output
    nc = ut.io.load('output/0.7.2-craypetsc/cordillera-narr-5km/'
                    '%s3222cool%02d+ccyc4+till1545/y???????-extra.nc'
                     % (rec.replace(' ', '').lower(), round(100*dt)))
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
    warm = warm.sum(axis=0).T/10.0

    # set levels, colors and hatches
    levs = [-1] + range(0, 121, 20)
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
    nc.close()

    # add map elements
    ut.pl.draw_boot_topo(ax)
    ut.pl.draw_natural_earth(ax)
    ut.pl.add_corner_tag(ax, rec.upper())

# locate Skeena Mountains
ut.pl.add_pointer_tag(ax, 'SM', xy=(-2000e3, 1450e3), xytext=(-2350e3, 1450e3))
ut.pl.add_pointer_tag(ax, 'MKM', xy=(-1550e3, 2000e3), xytext=(-1200e3, 2000e3))

# add colorbar and save
cb = fig.colorbar(cs, cax, orientation='horizontal', ticks=levs[1:])
cb.set_label('duration of warm-based ice cover (ka)')
cax.get_xticklabels()[-1].set_ha('right')
ut.pl.savefig(fig)
