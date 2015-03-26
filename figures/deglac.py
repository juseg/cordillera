#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm, Normalize
from paperglobals import *

# parameters
res = '5km'
records = records[0:3:2]
offsets = offsets[0:3:2]
ages = range(8, 23, 1)
levs = [-0.5] + ages
cmap = plt.get_cmap('RdBu_r')
cmap.set_over(darkgreen)

# initialize figure
fig = iplt.gridfigure((47.5, 95.0), (1, len(records)), axes_pad=2.5*in2mm,
                      cbar_mode='single', cbar_pad=2.5*in2mm, cbar_size=5*in2mm)

# plot topographic map
draw_boot_topo(fig.grid, res)

# loop on records
for i, rec in enumerate(records):
    ax = fig.grid[i]
    ax.set_rasterization_zorder(2.5)
    this_run_path = run_path % (res, rec, offsets[i]*100)

    # read extra output
    print 'reading %s extra output...' % rec
    nc = ncopen(this_run_path + '-extra.nc')
    x = nc.variables['x']
    y = nc.variables['y']
    time = nc.variables['time']
    thk = nc.variables['thk']

    # compute deglaciation age
    print 'computing deglaciation age...'
    wasicefree = np.ones_like(thk[0].T)*0
    readvance = np.ones_like(thk[0].T)*0
    deglacage = np.ones_like(thk[0].T)*-1.0
    for i, t in enumerate(time[:]*s2ka):
        print '[ %02.1f %% ]\r' % (100.0*i/len(time)),
        icy = (thk[i].T >= thkth)
        if -14.0 < t < -10.0:
            readvance = np.where(icy*wasicefree, 1, readvance)
            wasicefree = 1-icy
        deglacage = np.where(icy, -t, deglacage)

    # plot
    cs = ax.contourf(x[:], y[:], deglacage, levels=levs, cmap=cmap, alpha=0.75,
                     norm=BoundaryNorm(levs, 256), extend='max')
    #ax.contour(x[:], y[:], deglacage, levels=levs, colors='k', linewidths=0.25)
    ax.contourf(x[:], y[:], readvance, levels=[0.5, 1.5], colors='none', hatches=['//'])
    ax.contour(x[:], y[:], readvance, levels=[0.5, 1.5], colors='k', linewidths=0.25)
    ax.contour(x[:], y[:], deglacage, levels=[levs[-1]], colors='k', linewidths=0.25)
    ax.contour(x[:], y[:], deglacage, levels=[-0.5], colors='k',
	       linestyles='solid', linewidths=0.5)

    # annotate
    annotate(ax, rec.upper())

    # add profile lines
    for yp in [1.7e6, 1.4e6, 1.1e6, 0.8e6]:
        ax.plot([-2.4e6, -1.25e6], [yp, yp], 'k|',
                         lw=0.25, ls='--', dashes=(2, 2))

# add colorbar and save
print 'saving deglac...'
cb = fig.colorbar(cs, ax.cax, ticks=ages)
cb.set_label('Deglaciation age (kyr)')
fig.savefig('deglac')
nc.close()
