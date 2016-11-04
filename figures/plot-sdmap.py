#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1.axes_grid import ImageGrid
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import iris
import iris.plot as iplt

# projections
cal = ccrs.LambertConformal(
    central_longitude=-95.0, central_latitude=49.0,
    false_easting=0.0, false_northing=0.0,
    secant_latitudes=(49.0, 77.0), globe=None, cutoff=0)
proj = ccrs.NorthPolarStereo(central_longitude=-90.0)

# initialize figure
figw, figh = 80.0, 110.0
fig = plt.figure(0, (figw/25.4, figh/25.4))
rect = [2.5/figw, 17.5/figh, 75.0/figw, 90.0/figh]
ax = fig.add_axes(rect, projection=proj)
ax.set_xlim(-4125e3, 4125e3)  # 75*55 = 4125
ax.set_ylim(-5950e3, 3950e3)  # 90*55 = 4950
ax.set_rasterization_zorder(2.5)

# read SD data, select July North hemisphere
sd = iris.load_cube('data/era40.sat.day.5801.dev.monstd.nc')
sd = sd[6]
sd = sd[:180,:]

# plot
sdmax = sd.data.max()
levs = np.arange(0, sdmax, 0.5)
levs = np.append(levs, sdmax)
cs = iplt.contourf(sd, levels=levs, cmap='Purples')  #, alpha=0.75)
iplt.contour(sd, levels=levs, colors='k', linewidths=0.1)

# add Natural Earth elements
ax.coastlines(edgecolor='k', lw=0.25, resolution='50m')

# add modelling domain
xmin = -2.5e6
xmax = -1e6
ymin = 0
ymax = 3e6
x = [xmin, xmin, xmax, xmax, xmin]
y = [ymin, ymax, ymax, ymin, ymin]
ax.plot(x, y, 'k', lw=1.0, transform=cal, zorder=3)

# add colorbar
cax = fig.add_axes([2.5/figw, 10.0/figh, 1-5.0/figw, 5.0/figh])
cb = fig.colorbar(cs, cax=cax, orientation='horizontal',
                  ticks=range(6)+[sdmax], format='%.2g')
cb.set_label(u'July PDD standard deviation (K)')

# save
fig.savefig('plot-sdmap')
