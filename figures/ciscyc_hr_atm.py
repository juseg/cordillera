#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt
from matplotlib.colors import BoundaryNorm

# read atmosphere file
# FIXME: add unit conversion to iceplotlib
res = '5km'
nc = ut.io.load('input/atm/cordillera-narr-%s.nc' % res)
x = nc.variables['x']
y = nc.variables['y']
temp = nc.variables['air_temp']
prec = nc.variables['precipitation']

# initialize figure
figw, figh = 85.0, 120.0
fig, grid = iplt.subplots_mm(nrows=2, ncols=3, sharex=True, sharey=True,
                             figsize=(figw, figh),
                             left=2.5, right=2.5, bottom=15.0, top=2.5,
                             wspace=2.5, hspace=2.5, projection=ut.pl.proj)

# draw topo and coastline
ut.pl.draw_boot_topo(grid)
ut.pl.draw_coastline(grid)

# draw natural earth elements
for ax in grid.flat:
    ax.set_rasterization_zorder(2.5)
    ut.pl.draw_ne_vectors(ax)  # swap to geoaxes after that

# plot temperature
levs = range(-30, 31, 6)  # or [-30 ] + range(-20,21,5) + [30]
norm=BoundaryNorm(levs, 256)
for i in range(2):
    im = grid[i, 0].contourf(x[:], y[:], temp[6*i].T-273.15,
                             cmap='RdBu_r', levels=levs, norm=norm, alpha=0.75)
cax = fig.add_axes([2.5/figw, 7.5/figh, 25.0/figw, 5.0/figh])
cb = fig.colorbar(im, cax, orientation='horizontal')
cb.set_label(u'temperature (°C)')

# plot precipitation
levs = np.logspace(1/3., 3, 9).round(0)
norm = BoundaryNorm(levs, 256)
for i in range(2):
    im = grid[i, 1].contourf(x[:], y[:], prec[6*i].T*910/12.,
                             cmap='Greens', levels=levs, norm=norm, alpha=0.75)
cax = fig.add_axes([30.0/figw, 7.5/figh, 25.0/figw, 5.0/figh])
cb = fig.colorbar(im, cax, orientation='horizontal', ticks=levs[::2])
cb.set_label(r'precipitation (mm)')
nc.close()

# read standard deviation file
# FIXME: add unit conversion to iceplotlib
nc = ut.io.load('input/sd/cordillera-narr-%s.nc' % res)
x = nc.variables['x']
y = nc.variables['y']
stdv = nc.variables['air_temp_sd']

# plot standard deviation
levs = np.linspace(0.0, 12.0, 9)
norm = BoundaryNorm(levs, 256)
for i in range(2):
    im = grid[i, 2].contourf(x[:], y[:], stdv[6*i].T, cmap='Reds',
                             levels=levs, norm=norm, alpha=0.75)
cax = fig.add_axes([57.5/figw, 7.5/figh, 25.0/figw, 5.0/figh])
cb = fig.colorbar(im, cax, orientation='horizontal', ticks=levs[2::2])
cb.set_label(u'PDD SD (°C)')
nc.close()

# annotate
ut.pl.add_corner_tag(grid[0, 2], 'January')
ut.pl.add_corner_tag(grid[1, 2], 'July')

# save
ut.pl.savefig(fig)
