#!/usr/bin/env python2
# coding: utf-8

import sys

sys.path.append('iceplotlib')

import os
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from iceplotlib import plot as iplt
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader

# file path
filename = (os.environ['HOME'] + '/pism/output/0.5.12/cordillera-narr-3km-bl/'
            'stepcool07sll120+ccli+till1030/y0010000-extra.nc')
t = 10e3
print filename

# Canadian Atlas Lambert projection
proj = ccrs.LambertConformal(
    central_longitude=-95.0, central_latitude=49.0,
    false_easting=0.0, false_northing=0.0,
    standard_parallels=(49.0, 77.0), globe=None, cutoff=0)

# prepare figure
figw, figh = 112.5, 225.0
fig = plt.figure(0, (figw/25.4, figh/25.4))
ax  = fig.add_axes([0, 0, 1, 1], projection=proj)
ax.outline_patch.set_linewidth(2.0)  # only with cartopy
nc = iplt.load(filename)

# bed topography
im = iplt.imshow(nc, 'topg', t=t, zorder=0)
iplt.shading(nc, 'topg', t=t, zorder=0)

# frozen bed areas
cs = iplt.contourf(nc, 'temppabase', t=t, levels=[-50.0, -1e-6], zorder=1,
                   cmap=None, colors='none', hatches=['//'])
cs = iplt.contour(nc, 'temppabase', t=t, levels=[-50.0, -1e-6], zorder=1,
                  cmap=None, colors='k', linewidths=0.25, linestyles=['-'])

# surface velocity
im = iplt.imshow(nc, 'csurf', t=t, cmap='Blues', alpha=0.75, zorder=2)

# surface topography
cs = iplt.contour(nc, 'usurf', t=t, levels=range(100, 6000, 100),
                  cmap=None, colors='k', linewidths=0.10, zorder=3)
cs = iplt.contour(nc, 'usurf', t=t, levels=range(1000,6000,1000),
                  cmap=None, colors='k', linewidths=0.25, zorder=3)
cs.clabel(fontsize=6, fmt='%g', linewidths=0.5)

# ice margin
cs = iplt.icemargin(nc, t=t, linewidths=0.5, zorder=4)
nc.close()

# Dyke margin
sf = shpreader.Reader('../data/external/ice14k.shp')
for rec in sf.records():
    if rec.attributes['SYMB'] == 'ICE':
        ax.add_geometries(rec.geometry, proj,
                          edgecolor='#800000', facecolor='none', zorder=0.5)

# colorbars
cax = fig.add_axes([5/figw, 10/figh, 2.5/figw, 40/figh])
cb = plt.colorbar(im, cax=cax)
cb.set_label('ice surface velocity (m/a)')

# save
fig.savefig('plot-lgm.png')
