#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm, LogNorm, Normalize
from matplotlib.colorbar import ColorbarBase
from paperglobals import *

# parameters
res = '6km'
records = ['grip', 'epica']
offsets = [5.8, 5.6]
tmin, tmax = -22.0, -8.0
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
    ax.set_rasterization_zorder(2.5)
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
    slidage = np.ones_like(mask[0])*-1.0
    glaciated = np.zeros_like(mask[0])
    lastu = np.zeros_like(u[0])
    lastv = np.zeros_like(v[0])
    imin, imax = [np.argmin(np.abs(time[:]*s2ka-t)) for t in (tmin, tmax)]
    for i in range(imin, imax+1):
        print '[ %02.1f %% ]\r' % (100.0*(i-imin)/(imax-imin)),
        icy = (mask[i] == 2)
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

    # plot parameters
    cmap='RdBu_r'
    norm=Normalize(-tmax, -tmin)
    plotres=12  # in km

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

    # add profile lines
    for yp in [1.7e6, 1.4e6, 1.1e6, 0.8e6]:
        ax.plot([-2.4e6, -1.25e6], [yp, yp], 'k|',
                         lw=0.25, ls='--', dashes=(2, 2))

    # annotate
    annotate(ax, rec.upper())

# locate Liard Lowland and Fraser Plateau
txtkwa = dict(ha='center', va='center',
              bbox=dict(ec='k', fc='w', alpha=1.0),
              arrowprops=dict(arrowstyle="->"))
ax.set_rasterization_zorder(2.5)
ax.annotate('LL', xy=(-1700e3, 1600e3), xytext=(-1100e3, 1600e3), **txtkwa)
ax.annotate('FP', xy=(-1850e3, 900e3), xytext=(-1100e3, 900e3), **txtkwa)

# add colorbar and save
print 'saving...'
cb = ColorbarBase(ax.cax, cmap=cmap, norm=norm, ticks=range(8, 23, 2))
cb.set_label('Age of last basal sliding (kyr)')
fig.savefig('lastflow')
nc.close()
