#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as mplt
from matplotlib.colors import BoundaryNorm
from mpl_toolkits.axes_grid1.axes_grid import ImageGrid
from paperglobals import *

# read atmosphere file
res = '6km'
nc = Dataset(atm_file % res)
x = nc.variables['x']
y = nc.variables['y']
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
levs = range(-30, 31, 6)  # or [-30 ] + range(-20,21,5) + [30]
norm=BoundaryNorm(levs, 256)
for i in range(2):
    im = grid[0+3*i].contourf(x[:], y[:], temp[6*i].T-273.15, cmap='RdBu_r',
                              levels=levs, norm=norm, alpha=0.75)
cax = fig.add_axes([2.5/figw, 7.5/figh, 25.0/figw, 5.0/figh])
cb = fig.colorbar(im, cax, orientation='horizontal')
cb.set_label(u'Temperature (°C)')

# plot precipitation
print 'plotting precipitation maps...'
levs = np.logspace(1/3., 3, 9).round(0)
#levs = [2, 5, 10, 20, 50, 100, 200, 500, 1000]
norm = BoundaryNorm(levs, 256)
for i in range(2):
    im = grid[1+3*i].contourf(x[:], y[:], prec[6*i].T*1000/12., cmap='Greens',
                              levels=levs, norm=norm, alpha=0.75)
cax = fig.add_axes([30.0/figw, 7.5/figh, 25.0/figw, 5.0/figh])
cb = fig.colorbar(im, cax, orientation='horizontal', ticks=levs[::2])
cb.set_label(r'Precipitation (mm)')

# plot standard deviation
print 'plotting standard deviation maps...'
levs = np.linspace(0.0, 12.0, 9)
norm = BoundaryNorm(levs, 256)
for i in range(2):
    im = grid[2+3*i].contourf(x[:], y[:], stdv[6*i].T, cmap='Reds',
                              levels=levs, norm=norm, alpha=0.75)
cax = fig.add_axes([57.5/figw, 7.5/figh, 25.0/figw, 5.0/figh])
cb = fig.colorbar(im, cax, orientation='horizontal', ticks=levs[2::2])
cb.set_label(u'PDD SD (°C)')
nc.close()

# draw topo and coastline
draw_boot_topo(grid, res)
draw_coastline(grid, res)

# annotate
annotate(grid[2], 'January')
annotate(grid[5], 'July')

# save
fig.savefig('atm')
