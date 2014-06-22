#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm, LogNorm
from mpl_toolkits.axes_grid1.axes_grid import ImageGrid
from paperglobals import *

# parameters
res = '6km'
rec = 'epica'
dt = 5.6

# initialize figure
figw, figh = 120.0, 100.0
fig = plt.figure(0, (figw*in2mm, figh*in2mm))
rect1 = [2.5/figw, 2.5/figh, 47.5/figw, 95.0/figh]
rect2 = [52.5/figw, 2.5/figh, 56.25/figw, 95.0/figh]
grid = [None]*5
grid[0] = fig.add_axes(rect1)
grid[1:] = ImageGrid(fig, rect2, (2, 2), axes_pad=2.5*in2mm,
                 cbar_mode='single', cbar_location='right',
                 cbar_pad=2.5*in2mm, cbar_size=5.0*in2mm)
remove_ticks(grid)

# get LGM time
this_run_path = run_path % (res, rec, dt*100)
lgm_time = get_mis_times(this_run_path + '-ts.nc')[-1][-1]
plot_times = [lgm_time, -16, -14, -12, -10]

# load extra output
nc = Dataset(this_run_path + '-extra.nc')
time = nc.variables['time'][:]*s2ka

# round pltting times to nearest slice
plot_idces = [(np.abs(time[:]-t)).argmin() for t in plot_times]

# plot
for i, t in enumerate(plot_idces):
    print 'plotting %s kyr snapshot...' % time[t]
    ax = grid[i]
    iplt.imshow(nc, 'topg', t, ax=ax,
                cmap=topo_cmap, norm=topo_norm)
    iplt.icemargin(nc, t, ax=grid[i],
                   linewidths=0.5)
    iplt.contour(nc, 'usurf', t, ax=ax,
                 levels=range(200, 5000, 200),
                 cmap=None, colors='k', linewidths=0.1)
    iplt.contour(nc, 'usurf', t, ax=ax,
                 levels=range(1000, 5000, 1000),
                 cmap=None, colors='k', linewidths=0.25)
    im = iplt.imshow(nc, 'velsurf_mag', t, ax=ax,
                     cmap=vel_cmap, norm=vel_norm, alpha=0.75)
    annotate(ax, '%s kyr' % time[t])

# close extra file
nc.close()

# add colorbar and save
cb = fig.colorbar(im, ax.cax, extend='both', format='%i',
                  ticks=np.logspace(1, 3.5, 6))
cb.set_label(r'surface velocity ($m\,yr^{-1}$)', labelpad=-2.0)
print 'saving...'
fig.savefig('deglacshots-epica')
