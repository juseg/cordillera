#!/usr/bin/env python2
# coding: utf-8

import sys

sys.path.append('iceplot')

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm, LogNorm
from iceplot import plot as iplt

# file path
filename = '/home/julien/pism/output/cordillera-narr-6km-bl/' \
           'epica3222cool560+ccyc+till1545/y0120000-extra.nc'
t = -1

# initialize figure
fig = plt.figure(0, (80/25.4, 160/25.4))
ax  = fig.add_axes([0, 0, 1, 1])
ax.axis('off')

# load extra output
nc = Dataset(filename)
mask = nc.variables['mask']
x = nc.variables['x']
y = nc.variables['y']
w = (3*x[0]-x[1])/2
e = (3*x[-1]-x[-2])/2 - (x[-1]-x[-2])/2  # weird but works
n = (3*y[0]-y[1])/2
s = (3*y[-1]-y[-2])/2 - (y[-1]-y[-2])/2  # weird but works
c = nc.variables['velbase_mag']
c = np.ma.array(c[:], mask=(mask[:] != 2))
dist = c.sum(axis=0).T/10.0  # convert to km

# set levels, colors and hatches
levs = np.logspace(1.0, 4.5, 8)
cmap = plt.get_cmap('Reds')
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
#cb = fig.colorbar(cf, ax.cax, format='%i')
#cb.set_label('Cumulative basal displacement (km)')
fig.savefig('plot-erosion')
