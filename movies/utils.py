# Copyright (c) 2021, Julien Seguinot (juseg.github.io)
# Creative Commons Attribution-ShareAlike 4.0 International License
# (CC BY-SA 4.0, http://creativecommons.org/licenses/by-sa/4.0/)

"""Cordillera animation tools."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from iceplot import plot as iplt

# geographic projections
ll = ccrs.PlateCarree()
cal = ccrs.LambertConformal(central_longitude=-95.0, central_latitude=49.0,
                            false_easting=0.0, false_northing=0.0,
                            standard_parallels=(49.0, 77.0))
proj = cal  # FIXME replace proj by cal in scripts

# geographic regions
regions = {'cordillera': (-2500e3, -1000e3, 0e3, 3000e3)}  # model domain


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


def subplots_2_cax_ts_anim(extent='cordillera'):
    """Init figure with two subplots, bottom colorbar and timeseries."""
    figw, figh = 180.0, 120.0
    # FIXME use absplots
    fig, grid = iplt.subplots_mm(nrows=1, ncols=2, sharex=True, sharey=True,
                                 figsize=(figw, figh), projection=proj,
                                 left=0.0, right=60.0, bottom=0.0, top=0.0,
                                 wspace=0.0, hspace=0.0)
    prepare_axes(grid, extent=extent)
    cax = fig.add_axes([1-50.0/figw, 15.0/figh, 40.0/figw, 5.0/figh])
    tsax = fig.add_axes([1-50.0/figw, 30.0/figh, 40.0/figw, 80.0/figh])
    for ax in grid:
        ax.outline_patch.set_ec('none')
    for x in [1/3., 2/3.]:
        cax.plot([x, x], [0.0, 1.0], color='k', clip_on=False,
                 transform=fig.transFigure, zorder=3)
    return fig, grid, cax, tsax
