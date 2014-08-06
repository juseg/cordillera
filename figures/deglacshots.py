#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm, LogNorm
from mpl_toolkits.axes_grid1.axes_grid import ImageGrid
from paperglobals import *

# parameters
res = '6km'
records = ['grip', 'epica']
offsets = [5.8, 5.6]
tkalist = [-16, -14, -12, -10]

# initialize figure
fig = iplt.gridfigure((22.5, 45.0), (len(records), 4), axes_pad=2.5*in2mm,
                      cbar_mode='single', cbar_pad=2.5*in2mm, cbar_size=5*in2mm)

# loop on records
for i, rec in enumerate(records):
    this_run_path = run_path % (res, rec, offsets[i]*100)

    # load extra output
    nc = Dataset(this_run_path + '-extra.nc')
    time = nc.variables['time'][:]*s2ka

    # round plotting times to nearest slices
    idxlist = [(np.abs(time[:]-t)).argmin() for t in tkalist]

    # plot
    for j, t in enumerate(idxlist):
        print 'plotting %s at %s ka...' % (rec, time[t])
        ax = fig.grid[4*i+j]
        ax.set_rasterization_zorder(2.5)
        iplt.imshow(nc, 'topg', t, ax,
                    cmap=topo_cmap, norm=topo_norm)
        iplt.icemargin(nc, t, ax,
                       linewidths=0.5)
        iplt.contour(nc, 'usurf', t, ax,
                     levels=range(200, 5000, 200),
                     cmap=None, colors='k', linewidths=0.1)
        iplt.contour(nc, 'usurf', t, ax,
                     levels=range(1000, 5000, 1000),
                     cmap=None, colors='k', linewidths=0.25)
        im = iplt.imshow(nc, 'velsurf_mag', t, ax,
                         cmap=vel_cmap, norm=vel_norm, alpha=0.75)
        annotate(ax, '%s kyr' % time[t])

        # add profile lines
        for yp in [1.7e6, 1.4e6, 1.1e6, 0.8e6]:
            ax.plot([-2.4e6, -1.25e6], [yp, yp], 'k|',
                    lw=0.25, ls='--', dashes=(2, 2))

    # add record label
    annotate(ax, rec.upper(), bottom=True)

    # close extra file
    nc.close()

# add colorbar and save
cb = fig.colorbar(im, ax.cax, extend='both', format='%i',
                  ticks=np.logspace(1, 3.5, 6))
cb.set_label(r'surface velocity ($m\,yr^{-1}$)', labelpad=-2.0)
print 'saving...'
fig.savefig('deglacshots')