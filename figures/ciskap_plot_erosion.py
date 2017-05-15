#!/usr/bin/env python2
# coding: utf-8

import sys

sys.path.append('iceplotlib')

import os
import util as ut
import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm, LogNorm, Normalize
from iceplotlib import plot as iplt

# file path
filename = (os.environ['HOME'] + '/pism/output/0.7.2-craypetsc/cordillera-narr-5km/'
            'grip3222cool620+ccyc4+till1545/y???????-extra.nc')

# initialize figure
figw, figh = 80.0, 160.0
fig = plt.figure(0, (figw/25.4, figh/25.4))
ax  = fig.add_axes([0, 0, 1, 1])
ax.axis('off')

# load extra output
nc = iplt.load(filename)
mask = nc.variables['mask']
x = nc.variables['x']
y = nc.variables['y']
c = nc.variables['velbase_mag']
c = np.ma.array(c[:], mask=(mask[:] != 2))
dist = c.sum(axis=0).T/10.0  # convert to km

# set levels, colors and hatches
levs = np.logspace(1.0, 4.5, 8)
cmap = plt.get_cmap('Greys')
cols = cmap(np.linspace(0.0, 1.0, len(levs)+1))
hatches = ['//'] + ['']*len(levs)

# plot
cf = ax.contourf(x[:], y[:], dist, levels=levs,
                 colors=cols, hatches=hatches,
                 extend='both', alpha=0.75)
ax.contour(x[:], y[:], dist, levels=[levs[0]],
           colors='k', linewidths=0.25)
ax.contour(x[:], y[:], dist.mask, [0.5], colors='k', linewidths=0.5)

# close extra file
nc.close()

# add colorbar and save
cax = fig.add_axes([1-45/figw, 5/figh, 40/figw, 2.5/figh])
cb = fig.colorbar(cf, cax, format='%i', orientation='horizontal')
cb.set_label('Cumulative basal displacement (km)')
ut.pl.savefig(fig)
