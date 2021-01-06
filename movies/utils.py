# Copyright (c) 2021, Julien Seguinot (juseg.github.io)
# Creative Commons Attribution-ShareAlike 4.0 International License
# (CC BY-SA 4.0, http://creativecommons.org/licenses/by-sa/4.0/)

"""Cordillera animation tools."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import absplots as apl


# Figure creation
# ---------------

def subplots():
    """Init figure with two subplots, bottom colorbar and timeseries."""

    # geographic projection
    proj = ccrs.LambertConformal(central_longitude=-95, central_latitude=49,
                                 standard_parallels=(49, 77))

    # initialize figure
    fig, grid = apl.subplots_mm(
        ncols=2, nrows=1, sharex=True, sharey=True, figsize=(192, 108),
        subplot_kw=dict(projection=proj), gridspec_kw=dict(
            left=0, right=192-108, bottom=0, top=0, wspace=0))
    tsax = fig.add_axes_mm([108+10, 30, 192-108-20, 108-40])
    cax = fig.add_axes_mm([108+10, 15, 192-108-20, 5])

    # prepare map axes
    for i, ax in enumerate(grid):
        ax.set_extent([-2500e3, -1000e3, 0e3, 3000e3], crs=ax.projection)
        ax.outline_patch.set_ec('none')

    # add delimitors on last axes
    for i in range(2):
        ax.plot([i, i], [0, 1], color='k', clip_on=False,
                transform=ax.transAxes, zorder=3)

    return fig, grid, cax, tsax
