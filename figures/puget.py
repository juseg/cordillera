#!/usr/bin/env python2
# coding: utf-8

from paperglobals import *
from matplotlib.ticker import FuncFormatter

# initialize figure
times = np.arange(-23.0, -17.0, 0.5)
imin, imax = 70, 120
jmin, jmax = 35, 85
figw, figh = 120.0, 90.0
fig, grid = iplt.subplots_mm(nrows=3, ncols=4, sharex=True, sharey=True,
                             figsize=(figw, figh),
                             left=2.5, right=2.5, bottom=2.5, top=2.5,
                             wspace=2.5, hspace=2.5, projection='mapaxes')

# load extra output
print 'reading extra output...'
nc = open_extra_file('5km', 'grip', 6.1)

# loop on records[i]
for i, t in enumerate(times):

    # find nearest time slice
    k = np.argmin(np.abs(nc.variables['time'][:]*s2ka-t))

    # slice
    # FIXME: enable cropping in iceplotlib
    time = nc.variables['time'][k]*s2ka
    thk = nc.variables['thk'][k,imin:imax,jmin:jmax].T
    topg = nc.variables['topg'][k,imin:imax,jmin:jmax].T
    usurf = nc.variables['usurf'][k,imin:imax,jmin:jmax].T
    u = nc.variables['uvelsurf'][k,imin:imax,jmin:jmax].T
    v = nc.variables['vvelsurf'][k,imin:imax,jmin:jmax].T
    thk = nc.variables['thk'][k,imin:imax,jmin:jmax].T

    # apply masks
    icy = (thk >= thkth)
    usurf = np.ma.array(usurf, mask=(1-icy))
    u = np.sign(u)*np.log(1+np.abs(u)/100)
    v = np.sign(v)*np.log(1+np.abs(v)/100)
    c = (u**2 + v**2)**0.5

    # plot
    print 'plotting at %s ka...' % time
    ax = grid.flat[i]
    ax.set_rasterization_zorder(2.5)
    iplt.Axes.imshow(ax, topg-125.0, cmap=topo_cmap, norm=topo_norm)
    iplt.Axes.contour(ax, usurf, levels=range(100, 5000, 100),
                      colors='k', linewidths=0.2)
    iplt.Axes.contour(ax, usurf, levels=range(1000, 5000, 1000),
                      colors='k', linewidths=0.5)
    iplt.Axes.contourf(ax, icy, levels=[0.5, 1.5], colors='w', alpha=0.75)
    iplt.Axes.contour(ax, icy, levels=[0.5], colors='k')
    iplt.Axes.quiver(ax, u, v, c, cmap=vel_cmap, scale=25.0)
    add_corner_tag(ax, '%s ka' % (time))

# save
print 'saving puget...'
fig.savefig('puget')
nc.close()
