#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm, Normalize
from iceplot import plot as iplt
from paperglobals import *

# parameters
tmin, tmax = -19.5, -8.0

# initialize figure
figw, figh = 120.0, 85.0
fig, grid = plt.subplots(3, figsize=(120.0*in2mm, 85.0*in2mm),
                         sharex=True, sharey=True)
fig.subplots_adjust(left=10/figw, bottom=10/figh,
                    right=1-2.5/figw, top=1-2.5/figh,
                    wspace=2.5/figw, hspace=0.1)

# read extra output
print 'reading %s extra output...' % rec
nc = Dataset(run_path % ('10km', 'grip', 580) + '-extra.nc')
x = nc.variables['x']
y = nc.variables['y']
time = nc.variables['time']
mask = nc.variables['mask']
topg = nc.variables['topg']
usurf = nc.variables['usurf']

# plot
kmin, kmax = [np.argmin(np.abs(time[:]*s2ka-t)) for t in (tmin, tmax)]
for ax, yp in zip(grid, [2.0e6, 1.5e6, 1.0e6]):
    j = np.argmin(np.abs(y[:]-yp))
    xpf = x[:]*1e-3
    maskpf = mask[kmin:kmax, :, j]
    topgpf = topg[kmin:kmax, :, j]*1e-3
    surfpf = usurf[kmin:kmax, :, j]*1e-3
    #surfpf = np.ma.masked_where(maskpf != 2, surfpf)
    ax.grid(axis='y', c='0.5', ls='-', lw=0.1)
    ax.plot(xpf, surfpf.T, c=darkblue, lw=0.1)
    ax.plot(xpf, topgpf.T, c='k', lw=0.1)

# set axes properties
grid[0].set_xlim(-2.4e3, -1.25e3)  # shared
grid[0].set_ylim(-1, 4)  # shared
grid[0].set_yticks(range(4))  # shared
grid[1].set_ylabel('elevation (km)')
grid[2].set_xlabel('projection x-coordinate (km)')

# save
print 'saving...'
fig.savefig('profiles')
nc.close()
