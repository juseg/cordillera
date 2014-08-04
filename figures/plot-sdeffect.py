#!/usr/bin/env python2
# coding: utf-8

"""Plot effect of PDD standard deviation."""

import sys

sys.path.append('iceplot')

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1.axes_grid import ImageGrid
from iceplot import plot as iplt

# initialize figure
figw, figh = 170.0, 95.0
fig = plt.figure(0, (figw/25.4, figh/25.4))
rect = [2.5/figw, 5.0/figh, 165.0/figw, 88.75/figh]
grid = ImageGrid(fig, rect, (1, 4), axes_pad=2.5/25.4,
                 cbar_mode='each', cbar_location='bottom')
for ax in grid:
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

# loop on datasets
sdargs = ['+sd0', '+sd3', '', '+sdp']
mlist = []
zlist = []
for i, s in enumerate(sdargs):

    # plot
    nc = Dataset('/home/julien/pism/output/cordillera-narr-10km-bl/'
                   'stepcool07sll120+ccyc+till1545%s/y0010000.nc' % s)
    ax = grid[i]
    topo = iplt.imshow(nc, 'topg', 0, ax)
    iplt.shading(nc, 'topg', 0, ax)
    cs = iplt.contour(nc, 'usurf', 0, ax, levels=range(250, 6000, 250),
                      cmap=None, colors='k', linewidths=0.10)
    cs = iplt.contour(nc, 'usurf', 0, ax, levels=range(1000,6000,1000),
                      cmap=None, colors='k', linewidths=0.25)
    cs = iplt.icemargin(nc, 0, ax)

    # store mask and surface elevations
    mask = nc.variables['mask'][0].T
    mask = (mask == 0) + (mask == 4)
    mlist.append(mask)
    z = nc.variables['usurf'][0].T
    zlist.append(z)
    nc.close()

# plot anomalies
iref = 2
extent = topo.get_extent()
for i, ax in enumerate(grid):
    mask = mlist[i]*mlist[iref]
    diff = zlist[i]-zlist[iref]
    diff = np.ma.masked_where(mask, diff)
    maxdiff = (100 if i == 1 else 1000) #np.abs(diff).max()
    im = ax.imshow(diff, extent=extent, alpha=0.75,
                   cmap='RdBu', norm=Normalize(-maxdiff, maxdiff))
    if i != iref:
        cb = fig.colorbar(im, ax.cax, extend='both', orientation='horizontal',
                          ticks=np.linspace(-maxdiff, maxdiff, 5))
    else:
        ax.text(0.5, -0.12, r'elevation difference (m)',
                ha='center', transform=ax.transAxes)
        #cb = fig.colorbar(topo, ax.cax, extend='both', orientation='horizontal')
        #cb.set_label(r'bedrock elevation (m)')
        ax.cax.axis('off')


# add subfigure labels
for i, ax in enumerate(grid):
    ax.text(0.04, 0.96, '(%s)' % chr(97+i),
            fontweight='bold', transform=ax.transAxes)

# save
fig.savefig('plot-sdeffect')
