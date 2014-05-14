#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as mplt
from matplotlib.colors import LogNorm, Normalize
from mpl_toolkits.axes_grid1.axes_grid import ImageGrid

# file path
atm_file = '/home/julien/pism/input/atm/cordillera-narr-10km-bl.nc'

# read atmosphere file
nc = Dataset(atm_file)
temp = nc.variables['air_temp'][[5, 6, 7]].mean(axis=0).T
prec = nc.variables['precipitation'][[10, 11, 0]].mean(axis=0).T
stdv = nc.variables['air_temp_sd'][[5, 6, 7]].mean(axis=0).T
nc.close()

# initialize figure
mm = 1/25.4
figw, figh = 85.0, 70.0
fig = mplt.figure(0, (figw*mm, figh*mm))
rect = [2.5/figw, 10/figh, 80/figw, 57.5/figh]
grid = ImageGrid(fig, rect, (1, 3), axes_pad=2.5*mm,
                 cbar_mode='each', cbar_location='bottom',
                 cbar_pad=2.5*mm, cbar_size=5*mm)
for ax in grid:
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

# plot temperature
ax = grid[0]
im = ax.imshow(temp-273.15, cmap='YlOrRd', norm=Normalize(0, 30))
cb = fig.colorbar(im, ax.cax, orientation='horizontal', ticks=[0, 10, 20, 30])
cb.set_label('July temp.')

# plot precipitation
ax = grid[1]
im = ax.imshow(prec*1000/12., cmap='YlGnBu', norm=LogNorm(10, 800))
cb = fig.colorbar(im, ax.cax, orientation='horizontal', ticks=[20, 100, 400],
                  format='%g')
cb.set_label('Jan. precip.')

# plot standard deviation
ax = grid[2]
im = ax.imshow(stdv, cmap='RdPu', norm=Normalize(0, 6))
cb = fig.colorbar(im, ax.cax, orientation='horizontal', ticks=[0, 2, 4, 6])
cb.set_label('July std. dev.')

# save
fig.savefig('atm')
