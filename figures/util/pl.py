#!/usr/bin/env python2
# coding: utf-8

"""Plotting tools."""

import util as ut

import os
import numpy as np
import iceplotlib.plot as iplt
from matplotlib.transforms import ScaledTranslation

# unit conversion
in2mm = 1/25.4
pt2mm = 72*in2mm

def add_corner_tag(ax, s, ha='right', va='top'):
    fig = ax.get_figure()
    x = (ha == 'right')  # 0 for left edge, 1 for right edge
    y = (va == 'top')  # 0 for bottom edge, 1 for top edge
    xoffset = (1 - 2*x)*2.5*in2mm
    yoffset = (1 - 2*y)*2.5*in2mm
    offset = ScaledTranslation(xoffset, yoffset, fig.dpi_scale_trans)
    return ax.text(x, y, s, ha=ha, va=va,
                   bbox=dict(ec='k', fc='w', pad=1.25*pt2mm),
                   transform=ax.transAxes + offset)


def add_pointer_tag(ax, s, xy, xytext):
    return ax.annotate(s, xy=xy, xytext=xytext, ha='center', va='center',
                       xycoords='data', textcoords='data',
                       bbox=dict(ec='k', fc='w', boxstyle='square'),
                       arrowprops=dict(arrowstyle="->"))


def draw_boot_topo(grid, res):
    nc = ut.io.open_boot_file(res)
    for ax in grid.flat:
        im = nc.imshow('topg', ax=ax, cmap=ut.topo_cmap, norm=ut.topo_norm)
    nc.close()
    return im


def draw_coastline(grid, res):
    nc = ut.io.open_boot_file(res)
    for ax in grid.flat:
        cs = nc.contour('topg', ax=ax, levels=[0.0],
                        cmap=None, colors='k', linewidths=0.5)
    nc.close()
    return cs


def fig_hr_maps_mis(mis):

    # parameters
    res = '5km'
    records = ut.records[ut.hrs]
    offsets = ut.offsets[ut.hrs]

    # initialize figure
    figw, figh = 120.0, 100.0
    fig, grid = iplt.subplots_mm(nrows=1, ncols=2, sharex=True, sharey=True,
                                 figsize=(figw, figh),
                                 left=2.5, right=20.0, bottom=2.5, top=2.5,
                                 wspace=2.5, hspace=2.5)
    cax = fig.add_axes([1-17.5/figw, 2.5/figh, 5.0/figw, 1-5.0/figh])

    # loop on records
    for i, rec in enumerate(records):
        ax = grid[i]
        ax.set_rasterization_zorder(2.5)

        # get ice volume maximum
        t = ut.io.get_mis_times(res, rec, offsets[i])[-1][1-mis]

        # load extra output
        nc = ut.io.open_extra_file(res, rec, offsets[i])

        # plot
        print 'plotting %s at %.1f ka...' % (rec, -t/1e3)
        ax = grid[i]
        nc.imshow('topg', ax=ax, t=t,
                  cmap=ut.topo_cmap, norm=ut.topo_norm)
        nc.icemargin(ax=ax, t=t,
                     linewidths=0.5)
        nc.contour('usurf', ax=ax, t=t,
                   levels=range(200, 5000, 200),
                   cmap=None, colors='k', linewidths=0.1)
        nc.contour('usurf', ax=ax, t=t,
                   levels=range(1000, 5000, 1000),
                   cmap=None, colors='k', linewidths=0.25)
        im = nc.imshow('velsurf_mag', ax=ax, t=t,
                       cmap=ut.vel_cmap, norm=ut.vel_norm, alpha=0.75)
        ut.pl.add_corner_tag(ax, '%s, %.1f ka' % (rec.upper(), -t/1e3))

    # close extra file
    nc.close()

    # add colorbar and return figure
    cb = fig.colorbar(im, cax, extend='both', format='%i',
                      ticks=np.logspace(1, 3.5, 6))
    cb.set_label(r'surface velocity ($m\,yr^{-1}$)', labelpad=-2.0)
    return fig


def fig_hr_pf(res, rec, dt, color):

    # parameters
    tmin, tmax = -22.0, -8.0
    yplist = [1.7e6, 1.4e6, 1.1e6, 0.8e6]

    # initialize figure
    fig, grid = iplt.subplots_mm(len(yplist), figsize=(85.0, 100.0),
                                 sharex=True, sharey=True,
                                 left=10.0, bottom=10.0, right=2.5, top=2.5,
                                 hspace=2.5)

    # read extra output
    print 'reading %s extra output...' % rec
    nc = ut.io.open_extra_file(res, rec, dt)
    x = nc.variables['x']
    y = nc.variables['y']
    time = nc.variables['time']
    thk = nc.variables['thk']
    topg = nc.variables['topg']
    usurf = nc.variables['usurf']

    # plot
    kmin, kmax = [np.argmin(np.abs(time[:]*ut.s2ka-t)) for t in (tmin, tmax)]
    if kmin == kmax:  # run has not reached tmin yet
        return fig
    for i, yp in enumerate(yplist):
        ax = grid[i]
        ax.set_rasterization_zorder(2.5)
        j = np.argmin(np.abs(y[:]-yp))
        xpf = x[:]*1e-3
        maskpf = thk[kmin:kmax, :, j] < ut.thkth
        topgpf = topg[kmin:kmax, :, j]*1e-3
        surfpf = usurf[kmin:kmax, :, j]*1e-3
        surfpf = np.where(maskpf, topgpf, surfpf)  # apply topg where ice-free
        maskpf = np.roll(maskpf, -1) * np.roll(maskpf, 1)  # shrink mask by 1 cell
        surfpf = np.ma.masked_where(maskpf, surfpf)  # apply mask
        ax.grid(axis='y')
        ax.plot(xpf, surfpf.T, c=color, lw=0.1)
        ax.plot(xpf, topgpf.T, c='k', lw=0.1)
        ax.text(0.04, 0.84, chr(65+i), transform=ax.transAxes)
    nc.close()

    # set axes properties
    grid[0].set_xlim(-2.35e3, -1.3e3)  # shared
    grid[0].set_ylim(-1, 4)  # shared
    grid[0].set_yticks(range(4))  # shared
    grid[2].set_ylabel('elevation (km)')
    grid[-1].set_xlabel('projection x-coordinate (km)')

    # return produced figure
    return fig
