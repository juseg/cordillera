#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt
from matplotlib.colors import Normalize
from matplotlib.colorbar import ColorbarBase

# parameters
res = '5km'
records = ut.records[ut.hrs]
offsets = ut.offsets[ut.hrs]
tmin, tmax = -22.0, -8.0
cmap='RdBu_r'
norm=Normalize(-tmax, -tmin)
plotres=12  # in km

# initialize figure
figw, figh = 120.0, 100.0
fig, grid = iplt.subplots_mm(nrows=1, ncols=2, sharex=True, sharey=True,
                             figsize=(figw, figh),
                             left=2.5, right=20.0, bottom=2.5, top=2.5,
                             wspace=2.5, hspace=2.5)
cax = fig.add_axes([1-17.5/figw, 2.5/figh, 5.0/figw, 1-5.0/figh])

# plot topographic map
ut.pl.draw_boot_topo(grid, res)

# loop on records
for i, rec in enumerate(records):
    ax = grid[i]
    ax.set_rasterization_zorder(2.5)

    # read extra output
    print 'reading %s extra output...' % rec
    nc = ut.io.open_extra_file(res, rec, offsets[i])
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
    imin, imax = [np.argmin(np.abs(time[:]*ut.s2ka-t)) for t in (tmin, tmax)]
    if imin == imax:  # run has not reached tmin yet
        continue
    for i in range(imin, imax+1):
        print '[ %02.1f %% ]\r' % (100.0*(i-imin)/(imax-imin)),
        icy = (thk[i] >= ut.thkth)
        sliding = icy * (c[i].data > 1.0)
        lastu = np.where(sliding, u[i], lastu)
        lastv = np.where(sliding, v[i], lastv)
        slidage = np.where(sliding, -time[i]*ut.s2ka, slidage)
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
    ut.pl.add_corner_tag(ax, rec.upper())
    nc.close()

# locate Liard Lowland and Fraser Plateau
ax.set_rasterization_zorder(2.5)
ut.pl.add_pointer_tag(ax, 'LL', xy=(-1700e3, 1600e3), xytext=(-1100e3, 1600e3))
ut.pl.add_pointer_tag(ax, 'IP', xy=(-1850e3, 900e3), xytext=(-1100e3, 900e3))

# add colorbar and save
print 'saving...'
cb = ColorbarBase(cax, cmap=cmap, norm=norm, ticks=range(8, 23, 2))
cb.set_label('Age of last basal sliding (ka)')
fig.savefig('hr_geom_lastflow')
