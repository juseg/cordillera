#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt

# parameters
records = ut.hr.records
offsets = ut.hr.offsets
times = [-16e3, -14e3, -12e3, -10e3]

# initialize figure
figw, figh = 135.0, 115.0
fig, grid = iplt.subplots_mm(nrows=2, ncols=4, sharex=True, sharey=True,
                             figsize=(figw, figh), projection=ut.pl.proj,
                             left=2.5, right=17.5, bottom=2.5, top=2.5,
                             wspace=2.5, hspace=2.5)
cax = fig.add_axes([1-15.0/figw, 2.5/figh, 5.0/figw, 1-5.0/figh])

# loop on records
for i, rec in enumerate(records):
    dt = offsets[i]

    # load extra output
    nc = ut.io.load('output/0.7.2-craypetsc/cordillera-narr-5km/'
                    '%s3222cool%03d+ccyc4+till1545/y???????-extra.nc'
                     % (rec, round(100*dt)))

    # plot
    for j, t in enumerate(times):
        ax = grid[i, j]
        ax.set_rasterization_zorder(2.5)
        nc.imshow('topg', ax=ax, t=t, cmap=ut.topo_cmap, norm=ut.topo_norm,
                  zorder=-1)
        nc.contour('topg', ax=ax, t=t, levels=[0.0], cmap=None,
                   colors='0.25', linewidths=0.25, zorder=0)
        nc.icemargin(ax=ax, t=t, linewidths=0.5)
        nc.contour('usurf', ax=ax, t=t, levels=range(200, 5000, 200),
                   cmap=None, colors='k', linewidths=0.1)
        nc.contour('usurf', ax=ax, t=t, levels=range(1000, 5000, 1000),
                   cmap=None, colors='k', linewidths=0.25)
        im = nc.imshow('velsurf_mag', ax=ax, t=t,
                       cmap=ut.vel_cmap, norm=ut.vel_norm, alpha=0.75)
        ut.pl.draw_natural_earth(ax)
        ut.pl.add_corner_tag(ax, '%s ka' % (-t/1e3))

        # add profile lines
        for k, yp in enumerate([1.7e6, 1.4e6, 1.1e6, 0.8e6]):
            ax.plot([-2.4e6, -1.25e6], [yp, yp], 'k|',
                    lw=0.25, ls='--', dashes=(2, 2))
            if j==3:
                ax.text(-1.2e6, yp, chr(65+k), ha='left', va='bottom')

    # add record label
    ut.pl.add_corner_tag(ax, rec.upper(), va='bottom')

    # close extra file
    nc.close()

# add colorbar and save
cb = fig.colorbar(im, cax, extend='both', format='%i',
                  ticks=np.logspace(1, 3.5, 6))
cb.set_label(r'surface velocity ($m\,a^{-1}$)', labelpad=-2.0)
ut.pl.savefig(fig)
