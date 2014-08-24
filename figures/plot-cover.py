#!/usr/bin/env python2
# coding: utf-8

import sys

sys.path.append('iceplot')

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
from iceplot import plot as iplt
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader

# file path
filename = '/home/julien/pism/output/cordillera-narr-6km-bl/' \
           'grip3222cool580+ccyc+till1545/y0120000-extra.nc'
t = 1008
thkth=1.0

# prepare figure
figw, figh = 210.0, 165.0
fig = plt.figure(0, (figw/25.4, figh/25.4))
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')
ax.set_xlim((-2460e3, -1200e3))
ax.set_ylim((0e3, 990e3))

nc = Dataset(filename)
print nc.variables['time'][t]/(365.0 * 24 * 60 * 60 * 1000)

# bed topography
im = iplt.imshow(nc, 'topg', t, zorder=0)
iplt.shading(nc, 'topg', t, zorder=0)

# frozen bed areas
cs = iplt.contourf(nc, 'temppabase', t, thkth=thkth, levels=[-50.0, -1e-6],
                   cmap=None, colors='none', hatches=['//'], zorder=1)
cs = iplt.contour(nc, 'temppabase', t, thkth=thkth, levels=[-50.0, -1e-6],
                  cmap=None, colors='k', linewidths=0.25, linestyles=['-'],
                  zorder=1)

# ice margin
cs = iplt.icemarginf(nc, t, thkth=thkth, colors='w', alpha=0.85,  zorder=2)
cs = iplt.icemargin(nc, t, thkth=thkth, linewidths=0.5, zorder=2)

# surface topography
cs = iplt.contour(nc, 'usurf', t, thkth=thkth, levels=range(100, 6000, 100),
                  cmap=None, colors='k', linewidths=0.10, zorder=3)
cs = iplt.contour(nc, 'usurf', t, thkth=thkth, levels=range(1000,6000,1000),
                  cmap=None, colors='k', linewidths=0.25, zorder=3)
#cs.clabel(fontsize=6, fmt='%g', linewidths=0.5)

# surface velocity
qv = iplt.quiver(nc, 'velsurf', t, thkth=thkth,
                 cmap='Reds',
                 norm=LogNorm(10**1.5, 10**3.5),
                 scale=100.0, width=0.0005, zorder=4)

nc.close()

# colorbars
#cax = fig.add_axes([10/figw, 20/figh, 2.5/figw, 40/figh])
#cb = plt.colorbar(im, cax=cax)
#cb.set_label('ice surface velocity (m/a)')

# save
fig.savefig('plot-cover.png')
