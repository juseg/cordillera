#!/usr/bin/env python2
# coding: utf-8

import sys

sys.path.append('iceplot')

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as mplt
from matplotlib.colors import BoundaryNorm, Normalize
from mpl_toolkits.axes_grid1.axes_grid import ImageGrid
from iceplot import plot as iplt

# file paths
res = '10km'
pism_dir = '/home/julien/pism/'
atm_file = pism_dir + 'input/atm/cordillera-narr-%s-nn.nc' % res
boot_file = pism_dir + 'input/boot/cordillera-etopo1bed-%s.nc' % res

# read atmosphere file
nc = Dataset(atm_file)
x = nc.variables['x']
y = nc.variables['y']
temp = nc.variables['air_temp']
prec = nc.variables['precipitation']
stdv = nc.variables['air_temp_sd']

# initialize figure
figw, figh = 170.0, 100.0
fig = mplt.figure(0, (figw/25.4, figh/25.4))
rect = [2.5/figw, 10.0/figh, 165.0/figw, 88.75/figh]
grid = ImageGrid(fig, rect, (1, 4), axes_pad=2.5/25.4,
                 cbar_mode='each', cbar_location='bottom')
for ax in grid:
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

# plot mean temperature
print 'plotting temperature maps...'
levs = range(-15, 16, 3)  # or [-30 ] + range(-20,21,5) + [30]
cs = grid[0].contourf(x[:], y[:], temp[:].mean(axis=0).T-273.15,
                      levels=levs, norm=BoundaryNorm(levs, 256),
                      cmap='RdBu_r', alpha=0.75)
cb = fig.colorbar(cs, grid[0].cax, orientation='horizontal')
cb.set_label(u'Mean annual temperature (°C)')

# plot seasonality
levs = range(0, 51, 10)
cs = grid[1].contourf(x[:], y[:], (temp[:].max(axis=0)-temp[:].min(axis=0)).T,
                      levels=levs, norm=BoundaryNorm(levs, 256),
                      cmap='Oranges', alpha=0.75)
cb = fig.colorbar(cs, grid[1].cax, orientation='horizontal', ticks=levs[:-1])
cb.set_label(u'Temperature seasonality (°C)')

# plot mean precipitation
print 'plotting precipitation maps...'
levs = np.logspace(-1, 1, 7)
cs = grid[2].contourf(x[:], y[:], prec[:].mean(axis=0).T,
                      levels=levs, norm=BoundaryNorm(levs, 256),
                      cmap='Greens', alpha=0.75)
cb = fig.colorbar(cs, grid[2].cax, orientation='horizontal',
                  ticks=np.logspace(-1, 1, 3))
cb.set_label(u'Annual precipitation (m)')

# plot precipitation peak (0=DJF, 1=MAM, 2=JJA, 3=SON)
levs = np.arange(-0.5, 3.6)
cmap = mplt.get_cmap('Paired')
cols = cmap(np.linspace(0.0, 1.0, 12))
cols = cols[1:8:2]  # return all the darker tones b, g, r, o
cs = grid[3].contourf(x[:], y[:], (np.argmax(prec, axis=0).T+1)/3 % 4,
                      levels=levs, colors=cols, alpha=0.75)
cb = fig.colorbar(cs, grid[3].cax, orientation='horizontal', ticks=range(4))
cb.set_label(u'Precipitation peak season')
cb.ax.set_xticklabels(['DJF', 'MAM', 'JJA', 'SON'])

# close
nc.close()

# draw topo and coastline
nc = Dataset(boot_file)
for ax in grid:
    mplt.sca(ax)
    im = iplt.imshow(nc, 'topg',
                     cmap='Greys', norm=Normalize(-3000, 6000))
    cs = iplt.contour(nc, 'topg', levels=[0.0],
                      cmap=None, colors='k', linewidths=0.5)
# close
nc.close()

# save
fig.savefig('plot-atm')
