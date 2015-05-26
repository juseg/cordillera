#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm, LogNorm, Normalize
from matplotlib.colorbar import ColorbarBase
from paperglobals import *

# parameters
res = '5km'
records = records[0:3:2]
offsets = offsets[0:3:2]
tmin, tmax = -22.0, -8.0
cmap='RdBu_r'
norm=Normalize(-tmax, -tmin)
plotres=12  # in km

# initialize figure
fig = iplt.gridfigure((47.5, 95.0), (1, len(records)), axes_pad=2.5*in2mm,
                      cbar_mode='single', cbar_pad=2.5*in2mm, cbar_size=5*in2mm)

# plot topographic map
draw_boot_topo(fig.grid, res)

# loop on records
for i, rec in enumerate(records):
    ax = fig.grid[i]
    ax.set_rasterization_zorder(2.5)

    # read extra output
    print 'reading %s extra output...' % rec
    nc = open_extra_file(res, rec, offsets[i])
    x = nc.variables['x']
    y = nc.variables['y']
    time = nc.variables['time']
    thk = nc.variables['thk']
    u = nc.variables['uvelbase']
    v = nc.variables['vvelbase']
    c = nc.variables['velbase_mag']

    # compute last flow velocities
    print 'computing last flow velocities...'
    slidage = np.ones_like(thk[0])*-1.0
    glaciated = np.zeros_like(thk[0])
    lastu = np.zeros_like(u[0])
    lastv = np.zeros_like(v[0])
    imin, imax = [np.argmin(np.abs(time[:]*s2ka-t)) for t in (tmin, tmax)]
    if imin == imax:  # run has not reached tmin yet
        continue
    for i in range(imin, imax+1):
        print '[ %02.1f %% ]\r' % (100.0*(i-imin)/(imax-imin)),
        icy = (thk[i] >= thkth)
        sliding = icy * (c[i].data > 1.0)
        lastu = np.where(sliding, u[i], lastu)
        lastv = np.where(sliding, v[i], lastv)
        slidage = np.where(sliding, -time[i]*s2ka, slidage)
        glaciated = np.where(icy, 1, glaciated)

    # transpose and scale last flow velocity
    lastu = np.ma.masked_where(slidage < 0, lastu).T
    lastv = np.ma.masked_where(slidage < 0, lastv).T
    lastc = (lastu**2 + lastv**2)**0.5
    slidage = slidage.T
    glaciated = glaciated.T

    # plot last velocity stream lines
    print 'plotting...'
    ax.streamplot(x[:], y[:], lastu, lastv, color=slidage,
                  density=(60.0/plotres, 120.0/plotres),
                  cmap=cmap, norm=norm, linewidth=0.5)

    # plot glaciated and non-sliding areas
    ax.contourf(x[:], y[:], glaciated * (slidage < 0), levels=[0.5, 1.5],
                colors='none', hatches=['//'])
    ax.contour(x[:], y[:], slidage, levels=[0.0],
               colors='k', linewidths=0.25)
    ax.contour(x[:], y[:], glaciated, levels=[0.5],
               colors='k', linewidths=0.5)

    # annotate
    add_corner_tag(ax, rec.upper())
    nc.close()

# locate Liard Lowland and Fraser Plateau
ax.set_rasterization_zorder(2.5)
add_pointer_tag(ax, 'LL', xy=(-1700e3, 1600e3), xytext=(-1100e3, 1600e3))
add_pointer_tag(ax, 'IP', xy=(-1850e3, 900e3), xytext=(-1100e3, 900e3))

# add colorbar and save
print 'saving...'
cb = ColorbarBase(ax.cax, cmap=cmap, norm=norm, ticks=range(8, 23, 2))
cb.set_label('Age of last basal sliding (kyr)')
fig.savefig('lastflow')
