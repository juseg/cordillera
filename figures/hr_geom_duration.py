#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt

# simulations used
res = '5km'
records = ut.records[0:3:2]
offsets = ut.offsets[0:3:2]
cislevs = [32.0, 26.0]

# initialize figure
figw, figh = 120.0, 100.0
fig, grid = iplt.subplots_mm(nrows=1, ncols=2, sharex=True, sharey=True,
                             figsize=(figw, figh),
                             left=2.5, right=20.0, bottom=2.5, top=2.5,
                             wspace=2.5, hspace=2.5)
cax = fig.add_axes([1-17.5/figw, 2.5/figh, 5.0/figw, 1-5.0/figh])

# draw topo and coastline
ut.pl.draw_boot_topo(grid, res)

# loop on records[i]
for i, rec in enumerate(records):
    print 'reading %s extra output...' % rec
    ax = grid[i]
    ax.set_rasterization_zorder(2.5)

    # load extra output
    nc = ut.io.open_extra_file(res, rec, offsets[i])
    x = nc.variables['x']
    y = nc.variables['y']
    thk = nc.variables['thk']
    icecover = (thk[:] >= ut.thkth).sum(axis=0).T.astype('float')
    icecover *= 120.0/len(nc.variables['time'])

    # set contour levels, colors and hatches
    levs = range(0, 21, 5) + [cislevs[i]] + range(40,121,20)
    levs[0] = 1e-6
    cmap = iplt.get_cmap('RdBu')
    colors = cmap(np.hstack((np.linspace(0.0, 0.5, (len(levs)-1)/2),
                             np.linspace(0.5, 1.0, (len(levs)-1)/2))))
    hatches = ['']*5 + ['//'] + ['']*4

    # plot
    cf = ax.contourf(x[:], y[:], icecover, levels=levs, alpha=0.75,
                            colors=colors, hatches=hatches)
    cs = ax.contour(x[:], y[:], icecover, [cislevs[i]], colors='k',
                           linewidths=0.25)
    cs.clabel(fontsize=6, fmt='%i ka', manual=[(-1825e3, 1000e3)])
    ax.contour(x[:], y[:], icecover, [levs[0]],
                      colors='k', linewidths=0.5)

    # to display the first discontinuous contour
    #cs = ax.contour(x[:], y[:], icecover, [cislevs[i]+1.0],
    #                       colors='green', linewidths=0.25)

    # close extra file
    nc.close()
    ut.pl.add_corner_tag(ax, rec.upper())

# locate major mountain ranges
ut.pl.add_pointer_tag(ax, 'AR', xy=(-2300e3, 2600e3), xytext=(-2000e3, 2600e3))
ut.pl.add_pointer_tag(ax, 'SM', xy=(-2000e3, 1450e3), xytext=(-2350e3, 1450e3))
ut.pl.add_pointer_tag(ax, 'CM', xy=(-1950e3,  700e3), xytext=(-2350e3,  700e3))
ut.pl.add_pointer_tag(ax, 'NC', xy=(-1900e3, 250e3), xytext=(-2350e3, 250e3))
ut.pl.add_pointer_tag(ax, 'WSEM', xy=(-2200e3, 2150e3), xytext=(-1200e3, 2150e3))
ut.pl.add_pointer_tag(ax, 'SMKM', xy=(-1550e3, 1900e3), xytext=(-1200e3, 1900e3))
ut.pl.add_pointer_tag(ax, 'NRM', xy=(-1600e3, 1450e3), xytext=(-1200e3, 1450e3))
ut.pl.add_pointer_tag(ax, 'CRM', xy=(-1550e3,  650e3), xytext=(-1200e3,  650e3))

# add colorbar and save
cb = fig.colorbar(cf, cax)
cb.set_label('Duration of ice cover (ka)')
fig.savefig('hr_geom_duration')
