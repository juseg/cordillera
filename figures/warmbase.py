#!/usr/bin/env python2
# coding: utf-8

from paperglobals import *

# simulations used
res = '5km'
records = records[0:3:2]
offsets = offsets[0:3:2]

# initialize figure
figw, figh = 120.0, 100.0
fig, grid = iplt.subplots_mm(nrows=1, ncols=2, sharex=True, sharey=True,
                             figsize=(figw, figh),
                             left=2.5, right=20.0, bottom=2.5, top=2.5,
                             wspace=2.5, hspace=2.5, projection='mapaxes')
cax = fig.add_axes([1-17.5/figw, 2.5/figh, 5.0/figw, 1-5.0/figh])

# draw topo and coastline
draw_boot_topo(grid, res)

# loop on records[i]
for i, rec in enumerate(records):
    print 'reading %s extra output...' % rec
    ax = grid[i]
    ax.set_rasterization_zorder(2.5)

    # read extra output
    nc = open_extra_file(res, rec, offsets[i])
    x = nc.variables['x']
    y = nc.variables['y']
    w = (3*x[0]-x[1])/2
    e = (3*x[-1]-x[-2])/2 - (x[-1]-x[-2])/2  # weird but works
    n = (3*y[0]-y[1])/2
    s = (3*y[-1]-y[-2])/2 - (y[-1]-y[-2])/2  # weird but works
    thk = nc.variables['thk']
    temp = nc.variables['temppabase']

    # compute duration of warm-based coved
    warm = np.ma.array((temp[:] > -1e-9), mask=(thk[:] < thkth))
    warm = warm.sum(axis=0).T/10.0

    # set levels, colors and hatches
    levs = [-1] + range(0, 121, 20)
    cmap = iplt.get_cmap('Reds')
    colors = cmap(np.linspace(0.0, 1.0, len(levs)-1))
    hatches = ['//'] + ['']*(len(levs)-2)

    # draw contours
    cs = iplt.Axes.contourf(ax, x[:], y[:], warm, levels=levs, alpha=0.75,
                            colors=colors, hatches=hatches)
    iplt.Axes.contour(ax, x[:], y[:], warm, [0.0],
                      colors='k', linewidths=0.25)
    iplt.Axes.contour(ax, x[:], y[:], warm.mask, [0.5],
                      colors='k', linewidths=0.5)

    # close extra file
    add_corner_tag(ax, rec.upper())
    nc.close()

# locate Skeena Mountains
add_pointer_tag(ax, 'SM', xy=(-2000e3, 1450e3), xytext=(-2350e3, 1450e3))
add_pointer_tag(ax, 'MKM', xy=(-1550e3, 2000e3), xytext=(-1200e3, 2000e3))

# add colorbar and save
cb = fig.colorbar(cs, cax, ticks=levs[1:])
cb.set_label('Duration of warm-based ice cover (ka)')
fig.savefig('warmbase')
