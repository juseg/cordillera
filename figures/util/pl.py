# Copyright (c) 2014--2019, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# Creative Commons Attribution-ShareAlike 4.0 International License
# (CC BY-SA 4.0, http://creativecommons.org/licenses/by-sa/4.0/)

"""Plotting tools."""

import util as ut

import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as cshp


# Color palette
# -------------

# set color cycle to Colorbrewer Paired palette (l/d b/g/r/or/pu/br)
plt.rc('axes', prop_cycle=plt.cycler(color=plt.get_cmap('Paired').colors))


# Mapping properties
# ------------------

# velocity norm
velnorm = mpl.colors.LogNorm(1e1, 1e3)

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
# FIXME use absplots
in2mm = 1/25.4
pt2mm = 72*in2mm

# Iceplotlib functions
# --------------------

# FIXME use absplots instead of iceplotlib
# figure = iplt.figure
# subplots_mm = iplt.subplots_mm
# get_cmap = iplt.get_cmap


# Figures and axes creation
# -------------------------

def prepare_axes(grid=None, extent='cordillera', mis=True):
    """Prepare map and timeseries axes before plotting."""

    # prepare map axes
    for i, ax in enumerate(grid):
        ax.set_rasterization_zorder(2.5)
        ax.set_extent(regions[extent], crs=ax.projection)
        add_subfig_label('(%s)' % 'abcdefghijklmnopqrstuvwxyz'[i], ax=ax)

    # prepare timeseries axes
    # if tsax is not None:
    #     tsax.locator_params(axis='y', nbins=6)
    #     tsax.grid(axis='y')
    #     plot_dt(tsax)
    #     if mis is True:
    #         plot_mis(tsax)


def subplots_ts(nrows=1, ncols=1, figw=85.0):
    """Init figure with margins adapted for simple timeseries."""
    # FIXME use absplots
    figh = 30.0 + nrows*30.0
    return iplt.subplots_mm(nrows=nrows, ncols=ncols, figsize=(figw, figh),
                            sharex=True, sharey=False,
                            left=10.0, right=2.5, bottom=7.5, top=2.5,
                            hspace=2.5, wspace=2.5)


def subplots_2_cax(extent='cordillera'):
    """Init figure with two subplots and bottom colorbar."""
    figw, figh = 85.0, 95.0
    # FIXME use absplots
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
    # def add_corner_tag(text, ax=None, ha='right', va='top', offset=2.5/25.4):
    #     """Add text in figure corner."""
    #     return add_subfig_label(text, ax=ax, ha=ha, va=va, offset=offset)
    fig = ax.get_figure()
    x = (ha == 'right')  # 0 for left edge, 1 for right edge
    y = (va == 'top')  # 0 for bottom edge, 1 for top edge
    xoffset = (1 - 2*x)*offset
    yoffset = (1 - 2*y)*offset
    offset = mpl.transforms.ScaledTranslation(
        xoffset, yoffset, fig.dpi_scale_trans)
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
    ax = ax or plt.gca()
    x = (ha == 'right')  # 0 for left edge, 1 for right edge
    y = (va == 'top')  # 0 for bottom edge, 1 for top edge
    xoffset = (1 - 2*x)*offset
    yoffset = (1 - 2*y)*offset
    offset = mpl.transforms.ScaledTranslation(
        xoffset, yoffset, ax.figure.dpi_scale_trans)
    return ax.text(x, y, text, ha=ha, va=va, fontweight='bold',
                   transform=ax.transAxes + offset)


# Map elements
# ------------

def draw_lgm_outline(ax=None, c='#e31a1c'):
    """Draw LGM extent from Dyke (2004) deglacial outlines union"""
    # FIXME: compute union in preprocessing
    # available ages: 18.0, 17.5, 17.0, 16.5, 16.0, 15.5, 15.0, 14.5, 14.0,
    #                 13.5, 13.0, 12.5, 12.0, 11.5, 11.0, 10.5, 10.25, 10.0
    # calibrate ages: 21.4, 20.8, 20.2, 19.65, 19.1, 18.5, 17.9, 17.35, 16.8,
    #                 16.2, 15.6, 14.8, 14.1, 13.45, 13.0, 12.7, 12.0, 11.45
    raw_ages = [18.0, 17.0, 16.0, 15.0, 14.0]  # , 13.0, 12.0, 11.0, 10.0]
    # cal_ages = [21.4, 20.2, 19.1, 17.9, 16.8]  # , 15.6, 14.1, 13.0, 11.45]
    union = None
    for age in raw_ages:
        filename = '../data/external/ice%ik.shp' % age
        for rec in cshp.Reader(filename).records():
            if rec.attributes['SYMB'] == 'ICE':
                if union is None:
                    union = rec.geometry
                else:
                    union = union.union(rec.geometry)
    ax.add_geometries(union, cal, edgecolor=c, facecolor='none',
                      lw=0.5, alpha=0.75, zorder=0)


def draw_natural_earth(ax=None):
    """Add Natural Earth geographic data vectors."""
    ax = ax or plt.gca()
    ax.add_feature(rivers, zorder=0)
    ax.add_feature(lakes, zorder=0)
    ax.add_feature(graticules)


def draw_boot_topo(ax):
    nc = ut.io.load('input/boot/cordillera-etopo1bed-10km.nc')
    im = nc.imshow('topg', ax=ax, cmap='Greys', vmin=-3e6, vmax=6e6, zorder=-1)
    nc.contour('topg', ax=ax, levels=[0.0], colors='0.25',
               linewidths=0.25, zorder=0)
    nc.close()
    return im


# Saving figures
# --------------

def savefig(fig=None):
    """Save figure to script filename."""
    import sys
    fig = fig or plt.gcf()
    res = fig.savefig(os.path.splitext(sys.argv[0])[0])
    return res
