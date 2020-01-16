#!/usr/bin/env python
# Copyright (c) 2014--2020, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# Creative Commons Attribution-ShareAlike 4.0 International License
# (CC BY-SA 4.0, http://creativecommons.org/licenses/by-sa/4.0/)

"""
Plot CISCYC hires deglaciation snapshots.
"""

import util as ut
import xarray as xr
import absplots as apl


def main():
    """Main program called during execution."""

    # initialize figure
    fig, grid = apl.subplots_mm(
        figsize=(135, 115), nrows=2, ncols=4, gridspec_kw=dict(
            left=2.5, right=17.5, bottom=2.5, top=2.5, wspace=2.5, hspace=2.5),
        subplot_kw=dict(projection=ut.pl.proj))
    cax = fig.add_axes_mm([120, 2.5, 5, 110])

    # loop on records
    for i, rec in enumerate(ut.ciscyc_hr_records):

        # open postprocessed output
        ds = xr.load_dataset(
            '../data/processed/ciscyc.5km.{}.ex.1ka.nc'.format(rec.lower()))

        # plot
        innerlevs = [l for l in range(200, 5000, 200) if l % 1000 != 0]
        outerlevs = [l for l in range(200, 5000, 200) if l % 1000 == 0]
        for j, age in enumerate([16, 14, 12, 10]):
            ax = grid[i, j]
            ax.set_rasterization_zorder(2.5)
            snap = ds.sel(age=age)
            snap.topg.plot.imshow(
                ax=ax, add_colorbar=False, cmap=ut.topo_cmap,
                norm=ut.topo_norm, zorder=-1)
            snap.topg.plot.contour(
                ax=ax, levels=[0], colors='0.25', linewidths=0.25, zorder=0)
            snap.thk.notnull().plot.contour(
                ax=ax, colors='0.25', levels=[0], linewidths=0.5)
            (snap.topg+snap.thk).plot.contour(
                ax=ax, colors='0.25', levels=innerlevs, linewidths=0.1)
            (snap.topg+snap.thk).plot.contour(
                ax=ax, colors='0.25', levels=outerlevs, linewidths=0.25)
            ((snap.uvelsurf**2+snap.vvelsurf**2)**0.5).plot.imshow(
                ax=ax, alpha=0.75, cbar_ax=cax,
                cmap=ut.vel_cmap, norm=ut.vel_norm, cbar_kwargs=dict(
                    label=r'Surface velocity ($m\,a^{-1}$)',))

            # add map elements
            ax.set_title('')
            ut.pl.draw_natural_earth(ax)
            ut.pl.add_corner_tag(ax, '{} ka'.format(age))

            # add profile lines
            for k, yp in enumerate([1.7e6, 1.4e6, 1.1e6, 0.8e6]):
                ax.plot([-2.4e6, -1.25e6], [yp, yp], 'k|',
                        lw=0.25, ls='--', dashes=(2, 2))
                if j == 3:
                    ax.text(-1.2e6, yp, chr(65+k), ha='left', va='bottom')

        # add record label
        ut.pl.add_corner_tag(ax, rec.upper(), va='bottom')

    # add colorbar and save
    ut.pl.savefig(fig)


if __name__ == '__main__':
    main()
