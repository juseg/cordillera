#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm, Normalize
from iceplot import plot as iplt
from paperglobals import *

# parameters
res = '10km'
records = ['grip', 'epica']
offsets = [5.8, 5.6]

# initialize figure
fig = iplt.gridfigure((47.5, 95.0), (1, len(records)), axes_pad=2.5*in2mm,
                      cbar_mode='single', cbar_pad=2.5*in2mm, cbar_size=5*in2mm)

# loop on records
for i, rec in enumerate(records):
    ax = fig.grid[i]
    this_run_path = run_path % (res, rec, offsets[i]*100)

    # read extra output
    print 'reading %s extra output...' % rec
    nc = Dataset(this_run_path + '-extra.nc')
    x = nc.variables['x']
    y = nc.variables['y']
    time = nc.variables['time']
    mask = nc.variables['mask']

    # compute deglaciation age
    print 'computing deglaciation age...'
    wasicefree = np.ones_like(mask[0].T)*0
    readvance = np.ones_like(mask[0].T)*0
    deglacage = np.ones_like(mask[0].T)*-1.0
    for i, t in enumerate(time[:]*s2ka):
        print '[ %02.1f %% ]\r' % (100.0*i/len(time)),
        icy = (mask[i].T == 2)
        if -14.0 < t < -10.0:
            readvance = np.where(icy*wasicefree, 1, readvance)
            wasicefree = 1-icy
        deglacage = np.where(icy, -t, deglacage)

    # compute gradient
    deglacage = np.ma.masked_less(deglacage, 0.0)
    v, u = np.gradient(-deglacage)
    print u.min(), u.mean(), u.max()


    # plot
    ages = range(8, 23, 1)
    levs = [0] + ages
    ax.streamplot(x[:], y[:], u, v, color='k', density=(10, 20), linewidth=0.25)
    ax.contour(x[:], y[:], deglacage.mask, levels=[0.5], colors='k', linewidths=0.5)

    # annotate
    annotate(ax, rec.upper())

# add colorbar and save
print 'saving...'
fig.savefig('deglacgrad')
nc.close()