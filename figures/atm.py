#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as mplt
from matplotlib.colors import LogNorm, Normalize
from mpl_toolkits.axes_grid1.axes_grid import ImageGrid
from paperglobals import *

# read atmosphere file
res = '10km'
nc = Dataset(atm_file % res)
temp = nc.variables['air_temp']
prec = nc.variables['precipitation']
stdv = nc.variables['air_temp_sd']

# initialize figure
figw, figh = 85.0, 120.0
fig = mplt.figure(0, (figw*in2mm, figh*in2mm))
rect = [2.5/figw, 12.5/figh, 80/figw, 107.5/figh]
grid = ImageGrid(fig, rect, (2, 3), axes_pad=2.5*in2mm, cbar_mode='none')
remove_ticks(grid)

# plot temperature
print 'plotting temperature maps...'
im = grid[0].imshow(temp[0].T-273.15, cmap='Spectral_r', norm=Normalize(-30, 30))
im = grid[3].imshow(temp[6].T-273.15, cmap='Spectral_r', norm=Normalize(-30, 30))
cax = fig.add_axes([2.5/figw, 7.5/figh, 25.0/figw, 5.0/figh])
cb = fig.colorbar(im, cax, orientation='horizontal', ticks=[-30, 0, 30])
cb.set_label(u'Temperature (°C)')

# plot precipitation
print 'plotting precipitation maps...'
im = grid[1].imshow(prec[0].T*1000/12., cmap='YlGnBu', norm=LogNorm(10, 1000))
im = grid[4].imshow(prec[6].T*1000/12., cmap='YlGnBu', norm=LogNorm(10, 1000))
cax = fig.add_axes([30.0/figw, 7.5/figh, 25.0/figw, 5.0/figh])
cb = fig.colorbar(im, cax, orientation='horizontal', ticks=[20, 100, 400],
                  format='%g')
cb.set_label(r'Precipitation (mm)')


# plot standard deviation
print 'plotting standard deviation maps...'
im = grid[2].imshow(stdv[0].T, cmap='RdPu', norm=Normalize(0, 12))
im = grid[5].imshow(stdv[6].T, cmap='RdPu', norm=Normalize(0, 12))
cax = fig.add_axes([57.5/figw, 7.5/figh, 25.0/figw, 5.0/figh])
cb = fig.colorbar(im, cax, orientation='horizontal', ticks=[0, 6, 12])
cb.set_label(u'PDD SD (°C)')
nc.close()

# draw coastline
nc = Dataset(boot_file % res)
topg = nc.variables['topg']
for ax in grid:
    ax.contour(topg[:].T, levels=[0.0], colors='k')
nc.close()

# annotate
for i in range(3):
    annotate(grid[i+0], 'January')
    annotate(grid[i+3], 'July')

# save
fig.savefig('atm')
