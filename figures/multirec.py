#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as mplt
from mpl_toolkits.axes_grid1.axes_grid import ImageGrid
from iceplot import plot as iplt
from paperglobals import *

# simulations used
res = '20km'
records = ['grip', 'ngrip', 'epica', 'vostok', 'odp1012', 'odp1020']

# initialize snapshots figure
figw, figh = 122.51, 80.01
rect = [2.5/figw, 2.5/figh, 110/figw, 95/figh]
sn_fig = iplt.gridfigure((17.5, 35.0), (3, len(records)), axes_pad=2.5*in2mm,
                         cbar_mode='none', cbar_location='bottom',
                         cbar_pad=2.5*in2mm, cbar_size=5*in2mm)
sn_grid = sn_fig.grid

# get MIS indexes from TS file
mis_idces = np.zeros((len(records), 3), dtype=int)
mis_times = np.zeros((len(records), 3), dtype=int)

# loop on records[i]
for i, rec in enumerate(records):
    print 'reading %s extra output...' % rec

    # get MIS times
    mis_idces, mis_times = get_mis_times(run_path % (res, rec) + '-ts.nc')

    # load extra output
    nc = Dataset(run_path % (res, rec) + '-extra.nc')
    time = nc.variables['time'][:]*s2ka
    thk = nc.variables['thk']

    # round snapshot times to nearest slice
    mis_idces = [(np.abs(time[:]-t)).argmin() for t in mis_times]
    mis_times = time[mis_idces]

    # plot maps
    for j, t in enumerate(mis_idces):
        print 'plotting %s at %s...' % (rec, mis_times[j])
        ax = sn_grid[i+j*len(records)]
        mplt.sca(ax)
        iplt.bedtopoimage(nc, t)
        iplt.icemargincontour(nc, t)
        iplt.surftopocontour(nc, t, levels=range(250, 5000, 250),
                             linewidths=0.2)
        iplt.surftopocontour(nc, t, levels=range(1000, 5000, 1000))
        #im = iplt.surfvelimage(nc, t, alpha=0.5)
        mplt.text(13/15., 28/30., '%s kyr' % (mis_times[j]),
                 va='top', ha='right',
                 bbox=dict(ec='none', fc='w', alpha=0.75),
                 transform=ax.transAxes)

    # close extra file
    nc.close()

# add colorbar and save snapshots
print 'saving snapshots...'
#cb = sn_fig.colorbar(im, ax.cax, orientation='horizontal')
#cb.set_label(r'ice surface velocity ($m\,a^{-1}$)')
sn_fig.savefig('multirec')
