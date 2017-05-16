#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt

# simulations used
records = ut.hr.records
offsets = ut.hr.offsets
cislevs = [34.0, 28.0]

# initialize figure
fig, grid, cax = ut.pl.subplots_2_cax()

# draw topo and coastline
ut.pl.draw_boot_topo(grid)
ut.pl.draw_coastline(grid)

# loop on records[i]
for i, rec in enumerate(records):
    dt = offsets[i]
    ax = grid[i]
    ut.pl.draw_ne_vectors(ax)

    # load extra output
    nc = ut.io.load('output/0.7.2-craypetsc/cordillera-narr-5km/'
                    '%s3222cool%03d+ccyc4+till1545/y???????-extra.nc'
                    % (rec, round(100*dt)))
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
cb = fig.colorbar(cf, cax, orientation='horizontal')
cb.set_label('duration of glaciation (ka)')
cax.get_xticklabels()[0].set_ha('left')
cax.get_xticklabels()[-1].set_ha('right')
ut.pl.savefig(fig)
