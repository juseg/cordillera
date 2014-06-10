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
yplist = [1.7e6, 1.4e6, 1.1e6, 0.8e6]

# initialize figure
figw, figh = 120.0, 100.0
fig, grid = plt.subplots(len(yplist), figsize=(120.0*in2mm, 85.0*in2mm),
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
for ax, yp in zip(grid, yplist):
    j = np.argmin(np.abs(y[:]-yp))
    xpf = x[:]*1e-3
    maskpf = mask[kmin:kmax, :, j] != 2
    topgpf = topg[kmin:kmax, :, j]*1e-3
    surfpf = usurf[kmin:kmax, :, j]*1e-3
    surfpf = np.where(maskpf, topgpf, surfpf)  # apply topg where ice-free
    maskpf = np.roll(maskpf, -1) * np.roll(maskpf, 1)  # shrink mask by 1 cell
    surfpf = np.ma.masked_where(maskpf, surfpf)  # apply mask
    ax.grid(axis='y', c='0.5', ls='-', lw=0.1)
    ax.plot(xpf, surfpf.T, c=darkblue, lw=0.1)
    ax.plot(xpf, topgpf.T, c='k', lw=0.1)
    ax.text(0.04, 0.8, 'y = %i km' % (yp*1e-3), transform=ax.transAxes)

# set axes properties
grid[0].set_xlim(-2.4e3, -1.25e3)  # shared
grid[0].set_ylim(-1, 4)  # shared
grid[0].set_yticks(range(4))  # shared
grid[2].set_ylabel('elevation (km)')
grid[-1].set_xlabel('projection x-coordinate (km)')

# save
print 'saving...'
fig.savefig('profiles')
nc.close()
