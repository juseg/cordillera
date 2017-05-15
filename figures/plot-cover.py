#!/usr/bin/env python2
# coding: utf-8

import sys

sys.path.append('iceplotlib')

import os
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
from iceplotlib import plot as iplt
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader

# file path
filename = (os.environ['HOME'] + '/pism/output/0.7.2-craypetsc/cordillera-narr-5km/'
            'grip3222cool620+ccyc4+till1545/y???????-extra.nc')
t = -19.1e3
thkth=1.0

# prepare figure
figw, figh = 210.0, 165.0
fig = plt.figure(0, (figw/25.4, figh/25.4))
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')
ax.set_xlim((-2460e3, -1200e3))
ax.set_ylim((0e3, 990e3))

nc = iplt.load(filename)

# bed topography
im = iplt.imshow(nc, 'topg', t=t, zorder=0)
iplt.shading(nc, 'topg', t=t, zorder=0)

# frozen bed areas
cs = iplt.contourf(nc, 'temppabase', t=t, thkth=thkth, levels=[-50.0, -1e-6],
                   cmap=None, colors='none', hatches=['//'], zorder=1)
cs = iplt.contour(nc, 'temppabase', t=t, thkth=thkth, levels=[-50.0, -1e-6],
                  cmap=None, colors='k', linewidths=0.25, linestyles=['-'],
                  zorder=1)

# ice margin
cs = iplt.icemarginf(nc, t=t, thkth=thkth, colors='w', alpha=0.85,  zorder=2)
cs = iplt.icemargin(nc, t=t, thkth=thkth, linewidths=0.5, zorder=2)

# surface topography
cs = iplt.contour(nc, 'usurf', t=t, thkth=thkth, levels=range(100, 6000, 100),
                  cmap=None, colors='k', linewidths=0.10, zorder=3)
cs = iplt.contour(nc, 'usurf', t=t, thkth=thkth, levels=range(1000,6000,1000),
                  cmap=None, colors='k', linewidths=0.25, zorder=3)
#cs.clabel(fontsize=6, fmt='%g', linewidths=0.5)

# surface velocity
qv = iplt.quiver(nc, 'velsurf', t=t, thkth=thkth,
                 cmap='Reds',
                 norm=LogNorm(10**1.5, 10**3.5),
                 scale=100.0, width=0.0005, zorder=4)

nc.close()

# colorbars
#cax = fig.add_axes([10/figw, 20/figh, 2.5/figw, 40/figh])
#cb = plt.colorbar(im, cax=cax)
#cb.set_label('ice surface velocity (m/a)')

# save
fig.savefig('plot-cover')
