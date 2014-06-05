#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm, LogNorm, Normalize
from iceplot import plot as iplt
from paperglobals import *

# parameters
res = '10km'
records = ['grip', 'epica']
offsets = [5.8, 5.6]
ages = range(8, 23, 1)
levs = [0] + ages
cmap = plt.get_cmap('RdBu_r')
cmap.set_over(darkgreen)

# initialize figure
fig = iplt.gridfigure((47.5, 95.0), (1, len(records)), axes_pad=2.5*in2mm,
                      cbar_mode='single', cbar_pad=2.5*in2mm, cbar_size=5*in2mm)

# plot topographic map
draw_boot_topo(fig.grid, res)

# loop on records
for i, rec in enumerate(records):
    ax = fig.grid[i]
    this_run_path = run_path % (res, rec, offsets[i]*100)

    # read extra output
    print 'reading %s extra output...' % rec
    nc = Dataset(this_run_path + '-extra.nc')
    x = nc.variables['x']
    y = nc.variables['y']
    time = nc.variables['time']
    mask = nc.variables['mask']
    u = nc.variables['uvelbase']
    v = nc.variables['vvelbase']
    c = nc.variables['velbase_mag']

    # compute last flow velocities
    print 'computing last flow velocities...'
    lastu = np.zeros_like(u[0].T)
    lastv = np.zeros_like(v[0].T)
    for i, t in enumerate(time[:]*s2ka):
        print '[ %02.1f %% ]\r' % (100.0*i/len(time)),
        icy = (mask[i].T == 2)
        #sliding = np.ma.masked_where(mask[i].T != 2, c[i].T > 1.0)
        sliding = icy * c[i].data.T > 1.0
        lastu = np.where(sliding, u[i].T, lastu)
        lastv = np.where(sliding, v[i].T, lastv)

    # scale last flow velocity
    lastu = np.ma.masked_equal(lastu, 0.0)
    lastv = np.ma.masked_equal(lastv, 0.0)
    lastc = (lastu**2 + lastv**2)**0.5
    lastu = np.sign(lastu)*np.log(1+np.abs(lastu)/100.)
    lastv = np.sign(lastv)*np.log(1+np.abs(lastv)/100.)
    direc = np.arctan(lastv/lastu)

    # plot
    print 'plotting...'
    #ax.quiver(x[:], y[:], lastu, lastv, lastc, scale=100,
    #          cmap=vel_cmap, norm=vel_norm)
    ax.streamplot(x[:], y[:], lastu, lastv, color=lastc, density=(5, 10),
                  cmap=vel_cmap, norm=vel_norm, linewidth=0.5)
    ax.contour(x[:], y[:], (mask[:] == 2).sum(axis=0).T, levels=[0.5],
               colors='k', linewidths=0.5)

    # annotate
    annotate(ax, rec.upper())

# add colorbar and save
print 'saving...'
#cb = fig.colorbar(cs, ax.cax, ticks=ages)
#cb.set_label('Deglaciation age (kyr)')
fig.savefig('lastflow')
nc.close()
