#!/usr/bin/env python2
# coding: utf-8

from util import *
from util.io import *
from util.pl import *
import iceplotlib.plot as iplt

# parameters
res = '5km'
records = records[0:3:2]
offsets = offsets[0:3:2]
times = [-16e3, -14e3, -12e3, -10e3]

# initialize figure
figw, figh = 120.0, 97.5
fig, grid = iplt.subplots_mm(nrows=2, ncols=4, sharex=True, sharey=True,
                             figsize=(figw, figh),
                             left=2.5, right=20.0, bottom=2.5, top=2.5,
                             wspace=2.5, hspace=2.5)
cax = fig.add_axes([1-17.5/figw, 2.5/figh, 5.0/figw, 1-5.0/figh])

# loop on records
for i, rec in enumerate(records):

    # load extra output
    nc = open_extra_file(res, rec, offsets[i])

    # plot
    for j, t in enumerate(times):
        print 'plotting %s at %.1f ka...' % (rec, -t/1e3)
        ax = grid[i, j]
        ax.set_rasterization_zorder(2.5)
        nc.imshow('topg', ax=ax, t=t, thkth=thkth, cmap=topo_cmap, norm=topo_norm)
        nc.icemargin(ax=ax, t=t, thkth=thkth, linewidths=0.5)
        nc.contour('usurf', ax=ax, t=t, thkth=thkth, levels=range(200, 5000, 200),
                   cmap=None, colors='k', linewidths=0.1)
        nc.contour('usurf', ax=ax, t=t, thkth=thkth, levels=range(1000, 5000, 1000),
                   cmap=None, colors='k', linewidths=0.25)
        im = nc.imshow('velsurf_mag', ax=ax, t=t, thkth=thkth,
                       cmap=vel_cmap, norm=vel_norm, alpha=0.75)
        add_corner_tag(ax, '%s ka' % (-t/1e3))

        # add profile lines
        for k, yp in enumerate([1.7e6, 1.4e6, 1.1e6, 0.8e6]):
            ax.plot([-2.4e6, -1.25e6], [yp, yp], 'k|',
                    lw=0.25, ls='--', dashes=(2, 2))
            if j==3:
                ax.text(-1.2e6, yp, chr(65+k), ha='left', va='bottom')

    # add record label
    add_corner_tag(ax, rec.upper(), va='bottom')

    # close extra file
    nc.close()

# add colorbar and save
cb = fig.colorbar(im, cax, extend='both', format='%i',
                  ticks=np.logspace(1, 3.5, 6))
cb.set_label(r'surface velocity ($m\,yr^{-1}$)', labelpad=-2.0)
print 'saving...'
fig.savefig('deglacshots')
