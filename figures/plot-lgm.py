#!/usr/bin/env python2
# coding: utf-8

import sys

sys.path.append('iceplot')

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from iceplot import plot as iplt

# file path
filename = '/home/julien/pism/archive/cordillera-climate-3km/' \
           'cordillera-narr-3km-bl/stepcool07sll120+ccli+till1030/' \
           'y0010000-extra.nc'
t = -1

# prepare figure
figw, figh = 112.5, 225.0
fig = plt.figure(0, (figw/25.4, figh/25.4))
ax  = fig.add_axes([0, 0, 1, 1])
ax.axis('off')
nc = Dataset(filename)

# bed topography
im = iplt.imshow(nc, 'topg', t, zorder=0)
iplt.shading(nc, 'topg', t, zorder=0)

# frozen bed areas
cs = iplt.contourf(nc, 'temppabase', t, levels=[-50.0, -1e-6], zorder=1,
                   cmap=None, colors='none', hatches=['//'])
cs = iplt.contour(nc, 'temppabase', t, levels=[-50.0, -1e-6], zorder=1,
                  cmap=None, colors='k', linewidths=0.25, linestyles=['-'])

# surface velocity
im = iplt.imshow(nc, 'csurf', t, cmap='Blues', alpha=0.75, zorder=2)

# surface topography
cs = iplt.contour(nc, 'usurf', t, levels=range(100, 6000, 100),
                  cmap=None, colors='k', linewidths=0.10, zorder=3)
cs = iplt.contour(nc, 'usurf', t, levels=range(1000,6000,1000),
                  cmap=None, colors='k', linewidths=0.25, zorder=3)
cs.clabel(fontsize=6, fmt='%g', linewidths=0.5)

# ice margin
cs = iplt.icemargin(nc, t)
nc.close()

# colorbars
cax = fig.add_axes([5/figw, 10/figh, 2.5/figw, 40/figh])
cb = plt.colorbar(im, cax=cax)
cb.set_label('ice surface velocity (m/a)')

# save
fig.savefig('plot-lgm')
