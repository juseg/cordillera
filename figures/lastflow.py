#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm, LogNorm, Normalize
from matplotlib.colorbar import ColorbarBase
from iceplot import plot as iplt
from paperglobals import *

# parameters
res = '6km'
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
    deglacage = np.ones_like(mask[0].T)*-1.0
    lastu = np.zeros_like(u[0].T)
    lastv = np.zeros_like(v[0].T)
    for i, t in enumerate(time[:]*s2ka):
        print '[ %02.1f %% ]\r' % (100.0*i/len(time)),
        icy = (mask[i].T == 2)
        sliding = icy * c[i].data.T > 1.0
        lastu = np.where(sliding, u[i].T, lastu)
        lastv = np.where(sliding, v[i].T, lastv)
        deglacage = np.where(icy, -t, deglacage)

    # scale last flow velocity
    lastu = np.ma.masked_where(deglacage < 0, lastu)
    lastv = np.ma.masked_where(deglacage < 0, lastv)
    lastc = (lastu**2 + lastv**2)**0.5

    # plot parameters
    cmap='RdBu_r'
    norm=Normalize(8.0, 22.0)
    plotres=10.0  # in km

    # plot last velocity stream lines
    print 'plotting...'
    ax.streamplot(x[:], y[:], lastu, lastv, color=deglacage,
                  density=(60.0/plotres, 120.0/plotres),
                  cmap=cmap, norm=norm, linewidth=0.5)

    # plot glaciated and non-sliding areas
    ax.contourf(x[:], y[:], (deglacage > 0) * (lastc == 0), levels=[0.5, 1.5],
                colors='none', hatches=['//'])
    ax.contour(x[:], y[:], (deglacage > 0) * (lastc == 0), levels=[0.5],
               colors='k', linewidths=0.25)
    ax.contour(x[:], y[:], deglacage > 0, levels=[0.5],
               colors='k', linewidths=0.5)

    # annotate
    annotate(ax, rec.upper())

# add colorbar and save
print 'saving...'
cb = ColorbarBase(ax.cax, cmap=cmap, norm=norm, ticks=range(8, 23, 2))
cb.set_label('Deglaciation age (kyr)')
fig.savefig('lastflow')
nc.close()
