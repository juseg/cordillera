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


# Color palette
# -------------

# color brewer Paired palette
colorkeys = [tone+hue
             for hue in ('blue', 'green', 'red', 'orange', 'purple', 'brown')
             for tone in ('light', 'dark')]
colorvals = iplt.get_cmap('Paired', 12)(range(12))
palette = dict(zip(colorkeys, colorvals))


# Mapping properties
# ------------------

# velocity norm
velnorm = iplt.matplotlib.colors.LogNorm(1e1, 1e3)

# contour levels
topolevs = range(0, 4000, 200)
inlevs = [l for l in topolevs if l % 1000 != 0]
utlevs = [l for l in topolevs if l % 1000 == 0]


# Geographic data
# ---------------

# geographic projections
ll = ccrs.PlateCarree()
cal = ccrs.LambertConformal(central_longitude=-95.0, central_latitude=49.0,
                            false_easting=0.0, false_northing=0.0,
                            standard_parallels=(49.0, 77.0))
proj = cal  # FIXME replace proj by cal in scripts

# geographic regions
regions = {'cordillera': (-2500e3, -1000e3, 0e3, 3000e3)}  # model domain

# cartopy features
rivers = cfeature.NaturalEarthFeature(
    category='physical', name='rivers_lake_centerlines', scale='50m',
    edgecolor='0.25', facecolor='none', lw=0.5)
lakes = cfeature.NaturalEarthFeature(
    category='physical', name='lakes', scale='50m',
    edgecolor='0.25', facecolor='0.85', lw=0.25)
coastline = cfeature.NaturalEarthFeature(
    category='physical', name='coastline', scale='50m',
    edgecolor='0.25', facecolor='none', lw=0.25)
graticules = cfeature.NaturalEarthFeature(
    category='physical', name='graticules_5', scale='50m',
    edgecolor='0.25', facecolor='none', lw=0.1)

# unit conversion
# FIXME: use subplots_mm instead
in2mm = 1/25.4
pt2mm = 72*in2mm

# Figures and axes creation
# -------------------------

def prepare_axes(grid=None, extent='cordillera', mis=True):
    """Prepare map and timeseries axes before plotting."""

    # prepare map axes
    for i, ax in enumerate(grid):
        ax.set_rasterization_zorder(2.5)
        ax.set_extent(regions[extent], crs=ax.projection)
        add_subfig_label('(%s)' % 'abcdefghijklmnopqrstuvwxyz'[i], ax=ax)

    ## prepare timeseries axes
    #if tsax is not None:
    #    tsax.locator_params(axis='y', nbins=6)
    #    tsax.grid(axis='y')
    #    plot_dt(tsax)
    #    if mis is True:
    #        plot_mis(tsax)


def subplots_2_cax(extent='cordillera'):
    """Init figure with two subplots and bottom colorbar."""
    figw, figh = 85.0, 95.0
    fig, grid = iplt.subplots_mm(nrows=1, ncols=2, sharex=True, sharey=True,
                                 figsize=(figw, figh), projection=cal,
                                 left=2.5, right=2.5, bottom=15.0, top=2.5,
                                 wspace=2.5, hspace=2.5)
    prepare_axes(grid, extent=extent)
    cax = fig.add_axes([2.5/figw, 7.5/figh, 1-5.0/figw, 5.0/figh])
    return fig, grid, cax


# Text annotations
# ----------------

def add_corner_tag(ax, s, ha='right', va='top', offset=2.5*in2mm):
# FIXME update to use same function as in Alps project
#def add_corner_tag(text, ax=None, ha='right', va='top', offset=2.5/25.4):
#    """Add text in figure corner."""
#    return add_subfig_label(text, ax=ax, ha=ha, va=va, offset=offset)
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


def add_subfig_label(text, ax=None, ha='left', va='top', offset=2.5/25.4):
    """Add figure label in bold."""
    ax = ax or iplt.gca()
    x = (ha == 'right')  # 0 for left edge, 1 for right edge
    y = (va == 'top')  # 0 for bottom edge, 1 for top edge
    xoffset = (1 - 2*x)*offset
    yoffset = (1 - 2*y)*offset
    offset = iplt.matplotlib.transforms.ScaledTranslation(
        xoffset, yoffset, ax.figure.dpi_scale_trans)
    return ax.text(x, y, text, ha=ha, va=va, fontweight='bold',
                   transform=ax.transAxes + offset)


# Map elements
# ------------

def draw_natural_earth(ax=None):
    """Add Natural Earth geographic data vectors."""
    ax = ax or iplt.gca()
    ax.add_feature(rivers, zorder=0)
    ax.add_feature(lakes, zorder=0)
    ax.add_feature(coastline, zorder=0)
    ax.add_feature(graticules)


def draw_boot_topo(ax):
    nc = ut.io.load('input/boot/cordillera-etopo1bed-10km.nc')
    im = nc.imshow('topg', ax=ax, cmap='Greys', vmin=-3e6, vmax=6e6, zorder=-1)
    cs = nc.contour('topg', ax=ax, levels=[0.0], colors='0.25',
                    linewidths=0.25, zorder=0)
    nc.close()
    return im


def make_geoaxes(ax):
    gax = ax.figure.add_axes(ax.get_position(), projection=proj)
    gax.background_patch.set_visible(False)
    gax.set_rasterization_zorder(2.5)
    gax.set_xlim(ax.get_xlim())
    gax.set_ylim(ax.get_ylim())
    return gax


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
    nc = ut.io.load('output/0.7.2-craypetsc/cordillera-narr-%s/'
                    '%s3222cool%03d+ccyc4+till1545/y0??0000-extra.nc'
                    % (res, rec.replace(' ', '').lower(), round(100*dt)))
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
    res = fig.savefig(os.path.splitext(sys.argv[0])[0])
    return res
