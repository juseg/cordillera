#!/usr/bin/env python2
# coding: utf-8

"""Plotting tools."""

import util as ut

import os
import sys
import numpy as np
import iceplotlib.plot as iplt
from matplotlib.transforms import ScaledTranslation
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# unit conversion
in2mm = 1/25.4
pt2mm = 72*in2mm

# geographic projection
proj = ccrs.LambertConformal(
    central_longitude=-95.0, central_latitude=49.0,
    false_easting=0.0, false_northing=0.0,
    standard_parallels=(49.0, 77.0), globe=None, cutoff=0)

def add_corner_tag(ax, s, ha='right', va='top', offset=2.5*in2mm):
    fig = ax.get_figure()
    x = (ha == 'right')  # 0 for left edge, 1 for right edge
    y = (va == 'top')  # 0 for bottom edge, 1 for top edge
    xoffset = (1 - 2*x)*offset
    yoffset = (1 - 2*y)*offset
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
        im = nc.imshow('topg', ax=ax, cmap=ut.topo_cmap, norm=ut.topo_norm,
                       zorder=-1)
    nc.close()


def draw_coastline(grid, res):
    nc = ut.io.open_boot_file(res)
    for ax in grid.flat:
        cs = nc.contour('topg', ax=ax, levels=[0.0], cmap=None,
                        colors='0.25', linewidths=0.25, zorder=0)
    nc.close()
    return cs


def make_geoaxes(ax):
    gax = ax.figure.add_axes(ax.get_position(), projection=proj)
    gax.background_patch.set_visible(False)
    gax.set_rasterization_zorder(2.5)
    gax.set_xlim(ax.get_xlim())
    gax.set_ylim(ax.get_ylim())
    return gax


def draw_ne_vectors(ax):
    bwu = 0.5
    scale = '50m'
    ax.add_feature(cfeature.NaturalEarthFeature(
        category='physical', name='rivers_lake_centerlines', scale=scale,
        edgecolor='0.25', facecolor='none', lw=1.0*bwu), zorder=0)
    ax.add_feature(cfeature.NaturalEarthFeature(
        category='physical', name='lakes', scale=scale,
        edgecolor='0.25', facecolor='0.85', lw=0.5*bwu), zorder=0)
    ax.add_feature(cfeature.NaturalEarthFeature(
        category='physical', name='graticules_5', scale=scale,
        edgecolor='0.25', facecolor='none', lw=0.25*bwu))


def fig_hr_maps_mis(mis):

    # parameters
    res = '5km'
    records = ut.hr.records
    offsets = ut.hr.offsets

    # initialize figure
    figw, figh = 85.0, 95.0
    fig, grid = iplt.subplots_mm(nrows=1, ncols=2, sharex=True, sharey=True,
                                 figsize=(figw, figh), projection=ut.pl.proj,
                                 left=2.5, right=2.5, bottom=15.0, top=2.5,
                                 wspace=2.5, hspace=2.5)
    cax = fig.add_axes([2.5/figw, 7.5/figh, 1-5.0/figw, 5.0/figh])

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
        nc.imshow('topg', ax=ax, t=t,
                  cmap=ut.topo_cmap, norm=ut.topo_norm, zorder=-1)
        ut.pl.draw_ne_vectors(ax)
        nc.contour('topg', ax=ax, t=t, levels=[0.0], cmap=None,
                   colors='0.25', linewidths=0.25, zorder=0)
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
    cb = fig.colorbar(im, cax, extend='both', orientation='horizontal',
                      format='%i', ticks=np.logspace(1, 3.5, 6))
    cb.set_label(r'surface velocity ($m\,a^{-1}$)', labelpad=-0.0)
    return fig


def fig_hr_pf(res, rec, dt, color):

    # parameters
    tmin, tmax = -22.0, -8.0
    yplist = [1.7e6, 1.4e6, 1.1e6, 0.8e6]

    # initialize figure
    fig, grid = iplt.subplots_mm(len(yplist), figsize=(85.0, 95.0),
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


def savefig(fig=None):
    """Save figure to script filename."""
    import sys
    fig = fig or gcf()
    res = fig.savefig(ut.io.os.path.splitext(sys.argv[0])[0])
    return res
