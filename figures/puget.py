#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm, LogNorm
from matplotlib.ticker import FuncFormatter
from mpl_toolkits.axes_grid1.axes_grid import ImageGrid
from iceplot import plot as iplt
from paperglobals import *

# initialize figure
times = np.arange(-23.0, -17.0, 0.5)
imin, imax = 60, 99
jmin, jmax = 30, 69
fig = iplt.gridfigure((25.0, 25.0), (4, 3), axes_pad=2.5*in2mm,
                      cbar_mode='none', cbar_location='bottom',
                      cbar_pad=2.5*in2mm, cbar_size=5*in2mm)

# load extra output
print 'reading extra output...'
this_run_path = run_path % ('6km', 'grip', 580)
nc = Dataset(this_run_path + '-extra.nc')

# loop on records[i]
for i, t in enumerate(times):

    # find nearest time slice
    k = np.argmin(np.abs(nc.variables['time'][:]*s2ka-t))

    # slice
    time = nc.variables['time'][k]*s2ka
    mask = nc.variables['mask'][k,imin:imax,jmin:jmax].T
    topg = nc.variables['topg'][k,imin:imax,jmin:jmax].T
    usurf = nc.variables['usurf'][k,imin:imax,jmin:jmax].T
    u = nc.variables['uvelsurf'][k,imin:imax,jmin:jmax].T
    v = nc.variables['vvelsurf'][k,imin:imax,jmin:jmax].T
    thk = nc.variables['thk'][k,imin:imax,jmin:jmax].T

    # apply masks
    icy = (mask == 2)
    usurf = np.ma.array(usurf, mask=(1-icy))
    u = np.sign(u)*np.log(1+np.abs(u)/100)
    v = np.sign(v)*np.log(1+np.abs(v)/100)
    c = (u**2 + v**2)**0.5

    # plot
    print 'plotting at %s kyr...' % time
    ax = fig.grid[i]
    ax.imshow(topg-125.0, cmap=topo_cmap, norm=topo_norm)
    ax.contour(usurf, levels=range(100, 5000, 100), colors='k', linewidths=0.2)
    ax.contour(usurf, levels=range(1000, 5000, 1000), colors='k', linewidths=0.5)
    ax.contourf(icy, levels=[0.5, 1.5], colors='w', alpha=0.75)
    ax.contour(icy, levels=[0.5], colors='k')
    ax.quiver(u, v, c, cmap=vel_cmap, scale=25.0)
    annotate(ax, '%s kyr' % (time))

# add colorbar and save
#cb = fig.colorbar(cs, ax.cax, ticks=levs[::2],
#                  format=FuncFormatter(lambda x, pos: '%g' % (x/1000.0)))
#cb.set_label(r'surface elevation (km)')  #, labelpad=-1.5*pt2mm)
print 'saving...'
fig.savefig('puget')
nc.close()
