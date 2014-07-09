#!/usr/bin/env python2
# coding: utf-8

import sys

sys.path.append('iceplot')

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from iceplot import plot as iplt

# file path
filename = '/home/julien/pism/archive/cordillera-climate-3km/' \
           'cordillera-narr-3km-bl/stepcool07sll120+ccli+till1030/' \
           'y0010000-extra.nc'
t = -1

# prepare figure
fig = plt.figure(0, (80/25.4, 160/25.4))
ax  = fig.add_axes([0, 0, 1, 1])
ax.axis('off')
nc = Dataset(filename)

# bed topography
im = iplt.imshow(nc, 'topg', t)

# velocity quiver (use old varnames {u,v}_ssa)
# this does not work because the mask variable is missing.
#qv = iplt.quiver(nc, 'velsurf', t, width=0.0005) #, scale = 250
#qv.set_rasterized(True)

# surface topography contours
#cs = iplt.contour(nc, 'usurf', t, levels=range(100, 6000, 100),
#                  cmap=None, colors='k', linewidths=0.1)
#cs = iplt.contour(nc, 'usurf', t, levels=range(1000,6000,1000),
#                  cmap=None, colors='k', linewidths=0.5)
#cs.clabel(fontsize=6, fmt='%g')

# ice margin
#cs = iplt.icemargin(nc, t)
nc.close()

# colorbars
#cax = fig.add_axes([20/800., 300/1600., 10/800., 200/1600.])
#cb = mplt.colorbar(im, cax=cax)
#cb.set_label('basal topography (m)')
#cax = fig.add_axes([60/800., 300/1600., 10/800., 200/1600.])
#cb = mplt.colorbar(qv, cax=cax)
#cb.set_label('ice surface velocity (m/a)')

# save
fig.savefig('plot-lgm')

