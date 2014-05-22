#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1.axes_grid import ImageGrid
from iceplot import plot as iplt
from paperglobals import *

# simulations used
res = '10km'

# initialize snapshots figure
figw, figh = 120.0, 102.5
fig = plt.figure(0, (figw*in2mm, figh*in2mm))
rect = [5.0/figw, 2.5/figh, 107.5/figw, 95.0/figh]
grid = ImageGrid(fig, rect, (3, len(records)), axes_pad=2.5*in2mm,
                 cbar_mode='single', cbar_location='right',
                 cbar_pad=2.5*in2mm, cbar_size=2.5*in2mm)
remove_ticks(grid)

# get MIS indexes from TS file
mis_idces = np.zeros((len(records), 3), dtype=int)
mis_times = np.zeros((len(records), 3), dtype=int)

# loop on records[i]
for i, rec in enumerate(records):
    print 'reading %s extra output...' % rec
    this_run_path = run_path % (res, rec, offsets[i]*100)

    # get MIS times
    mis_idces, mis_times = get_mis_times(this_run_path + '-ts.nc')

    # load extra output
    nc = Dataset(this_run_path + '-extra.nc')
    time = nc.variables['time'][:]*s2ka
    topg = nc.variables['topg']
    usurf = nc.variables['uvelsurf']
    vsurf = nc.variables['vvelsurf']
    thk = nc.variables['thk']

    # round snapshot times to nearest slice
    mis_idces = [(np.abs(time[:]-t)).argmin() for t in mis_times]
    mis_times = time[mis_idces]

    # plot maps
    for j, t in enumerate(mis_idces):
        print 'plotting %s at %s...' % (rec, mis_times[j])
        ax = grid[i+j*len(records)]
        plt.sca(ax)
        iplt.bedtopoimage(nc, t, cmap=topo_cmap, norm=topo_norm)
        iplt.icemargincontour(nc, t)
        iplt.surftopocontour(nc, t, levels=range(1000, 5000, 1000), lw=0.25)
        csurf = (usurf[t].T**2 + vsurf[t].T**2)**0.5
        im = ax.imshow(np.ma.array(csurf, mask=None),
                       cmap=vel_cmap, norm=vel_norm, alpha=0.75)
        annotate(ax, '%s kyr' % (mis_times[j]))

    # close extra file
    nc.close()

# add labels
for i, label in enumerate(labels):
    ax = grid[i]
    ax.text(0.5, 1.05, labels[i], ha='center', fontweight='bold',
            transform=ax.transAxes)
for j in range(3):
    ax = grid[j*len(records)]
    ax.text(-0.05, 0.5, 'MIS %i' % (4-j),
        ha='right', va='center', fontweight='bold', rotation='vertical',
        transform=ax.transAxes)

# add colorbar and save
cb = fig.colorbar(im, ax.cax)
cb.set_label(r'surface velocity ($m\,a^{-1}$)', labelpad=-1.5*pt2mm)
print 'saving snapshots...'
fig.savefig('snapshots')
