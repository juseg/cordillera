#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from paperglobals import in2mm, run_path, s2ka

# parameters
tmin, tmax = -22.0, -8.0
yplist = [1.7e6, 1.4e6, 1.1e6, 0.8e6]

def profiles(res, rec, dt, color):
    # initialize figure
    figw, figh = 85.0, 100.0
    fig, grid = plt.subplots(len(yplist), figsize=(figw*in2mm, figh*in2mm),
                             sharex=True, sharey=True)
    fig.subplots_adjust(left=10.0/figw, bottom=10/figh,
                        right=1-2.5/figw, top=1-2.5/figh,
                        hspace=1/((1+figh/2.5)/4-1))

    # read extra output
    print 'reading %s extra output...' % rec
    nc = Dataset(run_path % (res, rec, 100*dt) + '-extra.nc')
    x = nc.variables['x']
    y = nc.variables['y']
    time = nc.variables['time']
    mask = nc.variables['mask']
    topg = nc.variables['topg']
    usurf = nc.variables['usurf']

    # plot
    kmin, kmax = [np.argmin(np.abs(time[:]*s2ka-t)) for t in (tmin, tmax)]
    for ax, yp in zip(grid, yplist):
        ax.set_rasterization_zorder(2.5)
        j = np.argmin(np.abs(y[:]-yp))
        xpf = x[:]*1e-3
        maskpf = mask[kmin:kmax, :, j] != 2
        topgpf = topg[kmin:kmax, :, j]*1e-3
        surfpf = usurf[kmin:kmax, :, j]*1e-3
        surfpf = np.where(maskpf, topgpf, surfpf)  # apply topg where ice-free
        maskpf = np.roll(maskpf, -1) * np.roll(maskpf, 1)  # shrink mask by 1 cell
        surfpf = np.ma.masked_where(maskpf, surfpf)  # apply mask
        ax.grid(axis='y', c='0.5', ls='-', lw=0.1)
        ax.plot(xpf, surfpf.T, c=color, lw=0.1)
        ax.plot(xpf, topgpf.T, c='k', lw=0.1)
        ax.text(0.04, 0.8, 'y = %i km' % (yp*1e-3), transform=ax.transAxes)
    nc.close()

    # set axes properties
    grid[0].set_xlim(-2.35e3, -1.3e3)  # shared
    grid[0].set_ylim(-1, 4)  # shared
    grid[0].set_yticks(range(4))  # shared
    grid[2].set_ylabel('elevation (km)')
    grid[-1].set_xlabel('projection x-coordinate (km)')

    # return produced figure
    return fig
