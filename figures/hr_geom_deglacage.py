#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt
from matplotlib.colors import BoundaryNorm

# parameters
res = '5km'
records = ut.records[hrs]
offsets = ut.offsets[hrs]
ages = range(8, 23, 1)
levs = [-0.5] + ages
cmap = iplt.get_cmap('RdBu_r')
cmap.set_over(ut.colors[4])  # dark green

# initialize figure
figw, figh = 120.0, 100.0
fig, grid = iplt.subplots_mm(nrows=1, ncols=2, sharex=True, sharey=True,
                             figsize=(figw, figh),
                             left=2.5, right=20.0, bottom=2.5, top=2.5,
                             wspace=2.5, hspace=2.5)
cax = fig.add_axes([1-17.5/figw, 2.5/figh, 5.0/figw, 1-5.0/figh])

# plot topographic map
ut.pl.draw_boot_topo(grid, res)

# loop on records
for i, rec in enumerate(records):
    ax = grid[i]
    ax.set_rasterization_zorder(2.5)

    # read extra output
    print 'reading %s extra output...' % rec
    nc = ut.io.open_extra_file(res, rec, offsets[i])
    x = nc.variables['x']
    y = nc.variables['y']
    time = nc.variables['time']
    thk = nc.variables['thk']

    # compute deglaciation age
    print 'computing deglaciation age...'
    wasicefree = np.ones_like(thk[0].T)*0
    readvance = np.ones_like(thk[0].T)*0
    deglacage = np.ones_like(thk[0].T)*-1.0
    for i, t in enumerate(time[:]*ut.s2ka):
        print '[ %02.1f %% ]\r' % (100.0*i/len(time)),
        icy = (thk[i].T >= ut.thkth)
        if -14.0 < t < -10.0:
            readvance = np.where(icy*wasicefree, 1, readvance)
            wasicefree = 1-icy
        deglacage = np.where(icy, -t, deglacage)

    # plot
    cs = ax.contourf(x[:], y[:], deglacage, levels=levs,
                            cmap=cmap, alpha=0.75,
                            norm=BoundaryNorm(levs, 256), extend='max')
    ax.contourf(x[:], y[:], readvance, levels=[0.5, 1.5],
                       colors='none', hatches=['//'])
    ax.contour(x[:], y[:], readvance, levels=[0.5, 1.5],
                      colors='k', linewidths=0.25)
    ax.contour(x[:], y[:], deglacage, levels=[levs[-1]],
                      colors='k', linewidths=0.25)
    ax.contour(x[:], y[:], deglacage, levels=[-0.5],
                      colors='k', linestyles='solid', linewidths=0.5)

    # annotate
    ut.pl.add_corner_tag(ax, rec.upper())

    # add profile lines
    for k, yp in enumerate([1.7e6, 1.4e6, 1.1e6, 0.8e6]):
        ax.plot([-2.4e6, -1.25e6], [yp, yp], 'k|',
                         lw=0.25, ls='--', dashes=(2, 2))
        ax.text(-1.225e6, yp, chr(65+k), ha='left', va='bottom')

# mark location of the Omineca mountains
ut.pl.add_pointer_tag(grid[0], 'OM', xy=(-1800e3, 1400e3), xytext=(-1300e3, 1250e3))

# add colorbar and save
print 'saving deglac...'
cb = fig.colorbar(cs, cax, ticks=ages)
cb.set_label('Deglaciation age (ka)')
fig.savefig('hr_geom_deglacage')
nc.close()