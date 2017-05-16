#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt
from matplotlib.colors import BoundaryNorm

# parameters
records = ut.hr.records
offsets = ut.hr.offsets
ages = range(8, 23, 1)
levs = [-0.5] + ages
cmap = iplt.get_cmap('RdBu_r')
cmap.set_over(ut.lr.colors[4])  # dark green

# initialize figure
fig, grid, cax = ut.pl.subplots_2_cax()

# plot topographic map
ut.pl.draw_boot_topo(grid)
ut.pl.draw_coastline(grid)

# loop on records
for i, rec in enumerate(records):
    dt = offsets[i]
    ax = grid[i]

    # read extra output
    nc = ut.io.load('output/0.7.2-craypetsc/cordillera-narr-5km/'
                    '%s3222cool%03d+ccyc4+till1545/y???????-extra.nc'
                     % (rec, round(100*dt)))
    x = nc.variables['x']
    y = nc.variables['y']
    time = nc.variables['time']
    thk = nc.variables['thk']

    # compute deglaciation age
    age = -time[:]*ut.s2ka
    icy = (thk[:] >= 1.0)
    nlastfree = icy[::-1].argmax(axis=0)  # number of last free timesteps
    deglacage = (age[-nlastfree-1]+age[-nlastfree]) / 2

    # fill in always and never icy cases
    nevericy = (nlastfree == 0)*(icy[-1] == 0)
    alwaysicy = (nlastfree == 0)*(icy[-1] == 1)
    deglacage[alwaysicy] = age[-1]
    deglacage = np.ma.array(deglacage, mask=nevericy)

    # check if there was a readvance
    i0 = 1059  # 14 ka
    i1 = 1099  # 10 ka
    nadvances = (np.diff(icy[i0:i1], axis=0) > 0).sum(axis=0)
    readvance = nadvances > 1  # I don't understand why this is not 0

    # transpose
    deglacage = deglacage.T
    readvance = readvance.T

    # plot
    cs = ax.contourf(x[:], y[:], deglacage, levels=levs,
                            cmap=cmap, alpha=0.75,
                            norm=BoundaryNorm(levs, 256), extend='max')
    ax.contourf(x[:], y[:], readvance, levels=[0.5, 1.5],
                      colors='none', hatches=['//'])
    ax.contour(x[:], y[:], readvance, levels=[0.5],
                      colors='k', linewidths=0.25)
    ax.contour(x[:], y[:], deglacage, levels=[levs[-1]],
                      colors='k', linewidths=0.25)
    ax.contour(x[:], y[:], deglacage.mask, levels=[0.5],
                      colors='k', linestyles='solid', linewidths=0.5)

    # close extra file
    nc.close()

    # add map elements
    ut.pl.draw_natural_earth(ax)
    ut.pl.add_corner_tag(ax, rec.upper())

    # add profile lines
    for k, yp in enumerate([1.7e6, 1.4e6, 1.1e6, 0.8e6]):
        ax.plot([-2.4e6, -1.25e6], [yp, yp], 'k|',
                         lw=0.25, ls='--', dashes=(2, 2))
        ax.text(-1.225e6, yp, chr(65+k), ha='left', va='bottom')

# mark location of the Omineca mountains
ut.pl.add_pointer_tag(grid[0], 'OM', xy=(-1800e3, 1400e3), xytext=(-1300e3, 1250e3))

# add colorbar and save
cb = fig.colorbar(cs, cax, orientation='horizontal', ticks=ages)
cb.set_label('deglaciation age (ka)')
ut.pl.savefig(fig)
