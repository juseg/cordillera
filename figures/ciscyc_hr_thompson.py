#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt
from matplotlib.colors import Normalize, LogNorm
from matplotlib.transforms import ScaledTranslation

# simulations used
res = '5km'
records = ut.hr.records
offsets = ut.hr.offsets

# cropping window
imin, imax = 120, 180
jmin, jmax = 80, 140

# loop on records
for i, rec in enumerate(records):
    dt = offsets[i]

    # initialize figure
    times = np.arange(-15.0, 0.0, 0.25)
    figw, figh = 120.0, 90.0
    fig, grid = iplt.subplots_mm(nrows=3, ncols=4, sharex=True, sharey=True,
                                 figsize=(figw, figh),
                                 left=2.5, right=2.5, bottom=2.5, top=2.5,
                                 wspace=2.5, hspace=2.5)

    # open extra file
    filename = ('/home/juliens/pism/output/0.7.2-craypetsc/cordillera-narr-5km/'
                '%s3222cool%d+ccyc4+till1545/y0??0000-extra.nc'
                % (rec, round(100*dt)))
    nc = iplt.load(filename)

    for i, ax in enumerate(grid.flat):
        t = times[i]

        # find nearest time slice
        time = nc.variables['time'][:]*ut.s2ka
        k = np.argmin(np.abs(time-t))
        age = -time[k]

        # slice
        # FIXME: enable cropping in iceplotlib
        x = nc.variables['x'][imin:imax].T
        y = nc.variables['y'][jmin:jmax].T
        thk = nc.variables['thk'][k,imin:imax,jmin:jmax].T
        topg = nc.variables['topg'][k,imin:imax,jmin:jmax].T
        usurf = nc.variables['usurf'][k,imin:imax,jmin:jmax].T
        velbase = nc.variables['velbase_mag'][k,imin:imax,jmin:jmax].T

        # apply masks
        icy = (thk >= 1.0)
        usurf = np.ma.array(usurf, mask=(-icy))
        velbase = np.ma.array(velbase, mask=(-icy))

        # plot
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        ax.set_rasterization_zorder(2.5)
        ax.pcolormesh(x, y, topg, cmap=ut.topo_cmap, norm=ut.topo_norm)
        ax.pcolormesh(x, y, velbase, cmap=ut.vel_cmap, norm=ut.vel_norm)
        ax.contour(x, y, velbase, levels=[1, 10, 100],
                   colors='k', linewidths=0.2)
        #ax.contour(x, y, usurf, levels=range(100, 5000, 100),
        #           colors='k', linewidths=0.2)
        #cs = ax.contour(x, y, usurf, levels=range(1000, 5000, 1000),
        #                colors='k', linewidths=0.5)
        #cs.clabel(fmt='%d', fontsize=4)
        ax.contourf(x, y, icy, levels=[0.5, 1.5], colors='1', alpha=0.75)
        ax.contour(x, y, icy, levels=[0.5], colors='k')
        ut.pl.add_corner_tag(ax, '%.1f ka' % age, offset=0.0)

    # save
    ut.pl.savefig(fig)
    nc.close()
