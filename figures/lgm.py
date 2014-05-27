#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm, LogNorm
from mpl_toolkits.axes_grid1.axes_grid import ImageGrid
from iceplot import plot as iplt
from paperglobals import *

# parameters
res = '10km'
records = ['grip', 'epica']
offsets = [5.8, 5.6]
ages = range(8, 23, 1)
levs = [0] + ages

# initialize figure
fig = iplt.gridfigure((47.5, 95.0), (1, len(records)), axes_pad=2.5*in2mm,
                      cbar_mode='single', cbar_location='right',
                      cbar_pad=2.5*in2mm, cbar_size=5*in2mm)

# loop on records[i]
for i, rec in enumerate(records):
    print 'reading %s extra output...' % rec
    this_run_path = run_path % (res, rec, offsets[i]*100)

    # get LGM time
    lgm_time = get_mis_times(this_run_path + '-ts.nc')[-1][-1]

    # load extra output
    nc = Dataset(this_run_path + '-extra.nc')
    time = nc.variables['time'][:]*s2ka
    topg = nc.variables['topg']
    # csurf = nc.variables['velsurf_mag']  # I forgot that in the 10km runs
    usurf = nc.variables['uvelsurf']
    vsurf = nc.variables['vvelsurf']
    thk = nc.variables['thk']

    # round LGM times to nearest slice
    lgm_indx = (np.abs(time[:]-lgm_time)).argmin()
    lgm_time = time[lgm_indx]

    # plot
    print 'plotting %s at %s...' % (rec, lgm_time)
    ax = fig.grid[i]
    plt.sca(ax)
    iplt.bedtopoimage(nc, lgm_indx, cmap=topo_cmap, norm=topo_norm)
    iplt.icemargincontour(nc, lgm_indx)
    iplt.surftopocontour(nc, lgm_indx, levels=range(100, 5000, 100), linewidths=0.25)
    iplt.surftopocontour(nc, lgm_indx, levels=range(1000, 5000, 1000), linewidths=0.5)
    csurf = (usurf[lgm_indx].T**2 + vsurf[lgm_indx].T**2)**0.5
    im = ax.imshow(csurf, cmap=vel_cmap, norm=LogNorm(10**1.0, 10**3.5), alpha=0.75)
    annotate(ax, '%s, %s kyr' % (rec.upper(), lgm_time))

    # close extra file
    nc.close()

# add colorbar and save
cb = fig.colorbar(im, ax.cax, extend='both', format='%i',
                  ticks=np.logspace(1, 3.5, 6))
cb.set_label(r'surface velocity ($m\,yr^{-1}$)')
print 'saving...'
fig.savefig('lgm')
