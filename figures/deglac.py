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
records = ['grip', 'vostok']
ages = range(8, 23, 1)
levs = [0] + ages
cmap = plt.get_cmap('Spectral_r')
cmap.set_over('g')

# initialize figure
fig = iplt.gridfigure((45.0, 90.0), (1, len(records)), axes_pad=2.5*in2mm,
                      cbar_mode='single', cbar_pad=2.5*in2mm, cbar_size=5*in2mm)

# plot topographic map
nc = Dataset(boot_file % res)
x = nc.variables['x']
y = nc.variables['y']
topg = nc.variables['topg']
w = (3*x[0]-x[1])/2
e = (3*x[-1]-x[-2])/2
n = (3*y[0]-y[1])/2
s = (3*y[-1]-y[-2])/2
for ax in fig.grid:
    ax.imshow(topg[:].T, cmap='Greys', norm=Normalize(-3000, 6000),
              extent=(w, e, n, s))
nc.close()

# loop on records
for i, rec in enumerate(records):
    ax = fig.grid[i]

    # read extra output
    print 'reading %s extra output...' % rec
    nc = Dataset(run_path % (res, rec) + '-extra.nc')
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

    # plot
    cs = ax.contourf(x, y, deglacage, levels=levs, cmap=cmap, alpha=0.75,
                     norm=BoundaryNorm(levs, 256), extend='max')
    ax.contour(x, y, deglacage, levels=levs, colors='k', linewidths=0.25)
    ax.contourf(x, y, readvance, levels=[0.5, 1.5], colors='none', hatches='//')
    ax.contour(x, y, readvance, levels=[0.5, 1.5], colors='k', linewidths=0.25)
    ax.contour(x, y, deglacage, levels=[0], colors='k', linewidths=0.5, zorder=10)

# add colorbar and save
print 'saving deglac...'
cb = fig.colorbar(cs, ax.cax, ticks=ages)
cb.set_label('Deglaciation age (kyr)')
fig.savefig('deglac')
nc.close()
