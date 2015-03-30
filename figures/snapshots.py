#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import FuncFormatter
from mpl_toolkits.axes_grid1.axes_grid import ImageGrid
from paperglobals import *

# parameters
res = '10km'

# initialize snapshots figure
figw, figh = 120.0, 102.5
fig = plt.figure(0, (figw*in2mm, figh*in2mm))
rect = [5.0/figw, 2.5/figh, 107.5/figw, 95.0/figh]
grid = ImageGrid(fig, rect, (3, len(records)), axes_pad=2.5*in2mm,
                 cbar_mode='single', cbar_location='right',
                 cbar_pad=2.5*in2mm, cbar_size=2.5*in2mm)
remove_ticks(grid)

# loop on records[i]
for i, rec in enumerate(records):
    print 'reading %s extra output...' % rec

    # get MIS times
    mis_idces, mis_times = get_mis_times(res, rec, offsets[i])

    # load extra output
    nc = open_extra_file(res, rec, offsets[i])
    time = nc.variables['time'][:]*s2ka

    # round snapshot times to nearest slice
    mis_idces = [(np.abs(time[:]-t)).argmin() for t in mis_times]
    mis_times = time[mis_idces]

    # plot maps
    for j, t in enumerate(mis_idces):
        print 'plotting %s at %s...' % (rec, mis_times[j])
        ax = grid[i+j*len(records)]
        ax.set_rasterization_zorder(2.5)
        iplt.imshow(nc, 'topg', t, ax=ax, thkth=thkth,
                    cmap=topo_cmap, norm=topo_norm)
        iplt.icemargin(nc, t, ax=ax, thkth=thkth,
                       linewidths=0.5)
        levs = range(0, 4001, 500)
        cs = iplt.contourf(nc, 'usurf', t, ax=ax, thkth=thkth,
                     levels=levs, cmap='Blues_r',
                     norm=BoundaryNorm(levs, 256), alpha=0.75)
        iplt.contour(nc, 'usurf', t, ax=ax, thkth=thkth,
                     levels=range(0, 4001, 500),
                     cmap=None, colors='k', linewidths=0.1)
        iplt.contour(nc, 'usurf', t, ax=ax, thkth=thkth,
                     levels=range(1000, 5000, 1000),
                     cmap=None, colors='k', linewidths=0.25)
        annotate(ax, '%s kyr' % (mis_times[j]))

    # close extra file
    nc.close()

# add labels
for i, label in enumerate(labels):
    ax = grid[i]
    ax.text(0.5, 1.05, labels[i], ha='center',
            transform=ax.transAxes)
for j in range(3):
    ax = grid[j*len(records)]
    ax.text(-0.05, 0.5, 'MIS %i' % (4-j),
            ha='right', va='center', rotation='vertical',
            transform=ax.transAxes)

# mark location of the skeena mountains
grid[8].annotate('SM', xy=(-2000e3, 1450e3), xytext=(-1100e3, 1450e3),
                       ha='center', va='center',
                       bbox=dict(ec='k', fc='w', alpha=1.0),
                       arrowprops=dict(arrowstyle="->"))

# add colorbar and save
cb = fig.colorbar(cs, ax.cax, ticks=levs[::2],
                  format=FuncFormatter(lambda x, pos: '%g' % (x/1000.0)))
cb.set_label(r'surface elevation (km)')  #, labelpad=-1.5*pt2mm)
print 'saving snapshots...'
fig.savefig('snapshots')
