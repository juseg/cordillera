#!/usr/bin/env python2
# coding: utf-8

import util as ut
import iceplotlib.plot as iplt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import FuncFormatter

# initialize snapshots figure
figw, figh = 135.0, 117.5
fig, grid = iplt.subplots_mm(nrows=3, ncols=6, sharex=True, sharey=True,
                             figsize=(figw, figh), projection=ut.pl.proj,
                             left=5.0, right=12.5, bottom=2.5, top=5.0,
                             hspace=2.5, wspace=2.5)
cax = fig.add_axes([1-10.0/figw, 2.5/figh, 2.5/figw, 1-7.5/figh])

# loop on records[i]
for i, rec in enumerate(ut.ciscyc_lr_records):
    dt = ut.ciscyc_lr_offsets[i]

    # get MIS times
    mis_idces, mis_times = ut.io.get_mis_times('10km', rec, dt)

    # load extra output
    nc = ut.io.load('output/0.7.2-craypetsc/cordillera-narr-10km/'
                    '%s3222cool%03d+ccyc4+till1545/y???????-extra.nc'
                    % (rec.replace(' ', '').lower(), round(100*dt)))

    # plot maps
    for j, t in enumerate(mis_times):
        ax = grid[j, i]
        ax.set_rasterization_zorder(2.5)
        nc.imshow('topg', ax=ax, t=t,
                  cmap=ut.topo_cmap, norm=ut.topo_norm, zorder=-1)
        nc.contour('topg', ax=ax, t=t, levels=[0.0], cmap=None,
                   colors='0.25', linewidths=0.25, zorder=0)
        nc.icemargin(ax=ax, t=t,
                     linewidths=0.5)
        levs = range(0, 4001, 500)
        cs = nc.contourf('usurf', ax=ax, t=t,
                         levels=levs, cmap='Blues_r',
                         norm=BoundaryNorm(levs, 256), alpha=0.75)
        nc.contour('usurf', ax=ax, t=t,
                   levels=range(0, 4001, 500),
                   cmap=None, colors='k', linewidths=0.1)
        nc.contour('usurf', ax=ax, t=t,
                   levels=range(1000, 5000, 1000),
                   cmap=None, colors='k', linewidths=0.25)
        ut.pl.draw_natural_earth(ax)
        ut.pl.add_corner_tag(ax, '%.1f ka' % (-mis_times[j]/1e3))

    # close extra file
    nc.close()

# add labels
for i, label in enumerate(ut.ciscyc_lr_records):
    ax = grid[0, i]
    ax.text(0.5, 1.05, label, ha='center',
            transform=ax.transAxes)
for j in range(3):
    ax = grid[j, 0]
    ax.text(-0.05, 0.5, 'MIS %i' % (4-j),
            ha='right', va='center', rotation='vertical',
            transform=ax.transAxes)

# mark location of the skeena mountains
ut.pl.add_pointer_tag(grid[1, 2], 'SM', xy=(-2000e3, 1450e3), xytext=(-1100e3, 1450e3))

# add colorbar and save
cb = fig.colorbar(cs, cax, ticks=levs[::2],
                  format=FuncFormatter(lambda x, pos: '%g' % (x/1000.0)))
cb.set_label(r'surface elevation (km)')  #, labelpad=-1.5*pt2mm)
ut.pl.savefig(fig)
