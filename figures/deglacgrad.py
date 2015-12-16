#!/usr/bin/env python2
# coding: utf-8

import util as ut
import iceplotlib.plot as iplt

# parameters
res = '5km'
records = ut.records[0:3:2]
offsets = ut.offsets[0:3:2]

# initialize figure
figw, figh = 120.0, 100.0
fig, grid = iplt.subplots_mm(nrows=1, ncols=2, sharex=True, sharey=True,
                             figsize=(figw, figh),
                             left=2.5, right=20.0, bottom=2.5, top=2.5,
                             wspace=2.5, hspace=2.5)

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

    # compute deglaciation age
    print 'computing deglaciation age...'
    wasicefree = np.ones_like(thk[0].T)*0
    readvance = np.ones_like(thk[0].T)*0
    deglacage = np.ones_like(thk[0].T)*-1.0
    for i, t in enumerate(time[:]*ut.s2ka):
        print '[ %02.1f %% ]\r' % (100.0*i/len(time)),
        icy = (thk[i].T >= thkth)
        if -14.0 < t < -10.0:
            readvance = np.where(icy*wasicefree, 1, readvance)
            wasicefree = 1-icy
        deglacage = np.where(icy, -t, deglacage)

    # compute gradient
    deglacage = np.ma.masked_less(deglacage, 0.0)
    v, u = np.gradient(-deglacage)

    # plot
    ages = range(8, 23, 1)
    levs = [0] + ages
    ax.streamplot(x[:], y[:], u, v,
                         color='k', density=(10, 20), linewidth=0.25)
    ax.contour(x[:], y[:], deglacage.mask,
                      levels=[0.5], colors='k', linewidths=0.5)

    # annotate
    ut.pl.add_corner_tag(ax, rec.upper())

# add colorbar and save
print 'saving...'
fig.savefig('deglacgrad')
nc.close()
